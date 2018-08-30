def weather_parameters(year, month, day, validity, prof_file):
    u = []
    v = []
    wind = []
    hgt = []
    tmp_c = []
    tmp_k = []
    p = []
    records1 = []
    ca0 = 998.0  # specific heat capacity at constant pressure of dry air (J kg^-1 K^-1)
    g = 9.81
    N = []
    dTdZ = []
    H_plume = 20000  # This will be an input
    H_source = 1000  # This will be an input
    H_top = H_source + H_plume
    print('Opening file ' + prof_file)
    with open(prof_file, 'r') as f1:
        next(f1)
        nlines = 0
        for line in f1:
            nlines += 1
            records1.append(line.split('     '))
        for i in range(0, nlines):
            hgt.append(float(records1[i][0]))
            p.append(float(records1[i][1]))
            tmp_k.append(float(records1[i][2]))
            tmp_c.append(float(records1[i][3]))
            u.append(float(records1[i][4]))
            v.append(float(records1[i][5]))
            wind.append(float(records1[i][6]))
            N.append(0)
            dTdZ.append(0)

        # Calculate buoyancy frequency. The assumption has been made that the average N is calculated from the source height to the top plume height, as it is also done in FALL3D. Indeed, in Degruyter and Bonadonna the average is from 0, though I believe it should be from the source height...
    N_avg = 0
    V_avg = 0
    for i in range(nlines - 1, -1, -1):
        if i == nlines - 1:
            dTdZ[i] = (tmp_c[i] - tmp_c[i - 1]) / (hgt[i] - hgt[i - 1])
        elif i == 0:
            dTdZ[i] = (tmp_c[i + 1] - tmp_c[i]) / (hgt[i + 1] - hgt[i])
        else:
            dTdZ[i] = (tmp_c[i + 1] - tmp_c[i - 1]) / (hgt[i + 1] - hgt[i - 1])
        N[i] = (g ** 2 / (ca0 * tmp_c[nlines - 1])) * (1 + (ca0 / g) * dTdZ[i])
        if hgt[i] < H_source:
            i_H_source = i
    if hgt[0] < H_top:
        print('Warning! Plume height > maximum height of the weather data domain')
    elif hgt[nlines - 1] > H_top:
        print('Warning! Plume height < surface level')

    # Calculate average N and V over the plume height (from the source to the top)
    for i in range(i_H_source, -1, -1):
        if hgt[i] > H_top:
            break
        elif H_source < hgt[i] < H_top:
            if hgt[i - 1] > H_top:
                # Interpolate N to H_top
                slope_N = (N[i - 1] - N[i]) / (hgt[i - 1] - hgt[i])
                q_N = -hgt[i] * slope_N + N[i]
                N_H_top = q_N + slope_N * H_top
                # Interpolate V to H_top
                slope_V = (wind[i - 1] - wind[i]) / (hgt[i - 1] - hgt[i])
                q_V = -hgt[i] * slope_V + wind[i]
                V_H_top = q_V + slope_V * H_top

                N_avg = N_avg + 0.5 * (N[i] + N_H_top) * abs(hgt[i] - H_top)
                V_avg = V_avg + 0.5 * (wind[i] + V_H_top) * abs(hgt[i] - H_top)
            else:
                N_avg = N_avg + 0.5 * (N[i] + N[i - 1]) * abs(hgt[i] - hgt[i - 1])
                V_avg = V_avg + 0.5 * (wind[i] + wind[i - 1]) * abs(hgt[i] - hgt[i - 1])
        else:
            # Interpolate N to H_source
            slope_N = (N[i - 1] - N[i]) / (hgt[i - 1] - hgt[i])
            q_N = -hgt[i] * slope_N + N[i]
            N_H_source = q_N + slope_N * H_source
            # Interpolate V to H_source
            slope_V = (wind[i - 1] - wind[i]) / (hgt[i - 1] - hgt[i])
            q_V = -hgt[i] * slope_V + wind[i]
            V_H_source = q_V + slope_V * H_source
            # Interpolate P to H_source
            slope_P = (p[i - 1] - p[i]) / (hgt[i - 1] - hgt[i])
            q_P = -hgt[i] * slope_P + p[i]
            P_H_source = q_P + slope_P * H_source
            # Interpolate T to H_source
            slope_T = (tmp_k[i - 1] - tmp_k[i]) / (hgt[i - 1] - hgt[i])
            q_T = -hgt[i] * slope_T + tmp_k[i]
            T_H_source = q_T + slope_T * H_source

            N_avg = N_avg + 0.5 * (N[i - 1] + N_H_source) * abs(hgt[i - 1] - H_source)
            V_avg = V_avg + 0.5 * (wind[i - 1] + V_H_source) * abs(hgt[i - 1] - H_source)

    N_avg = N_avg / (H_top - H_source)
    N_avg = N_avg ** 0.5
    V_avg = V_avg / (H_top - H_source)

    # Woodhouse (2013) Ws parameter
    Ws = (1.44 * V_H_top) / (N_avg * H_top)
    # Open file to store weather parameter needed for calculating MER
    wt_par = 'weather_parameters_' + validity + '.txt'
    fwt_par = open(wt_par, 'w')
    fwt_par.write(
        'Atmospheric pressure at the source [Pa] = %8.5e\nAtmospheric temperature at the source [K] = %8.5e\n\nData needed for Degruyter & Bonadonna (2012) model\nPlume height-averaged buoyancy frequency [1/s] = %8.5e\nPlume height-averaged wind speed [m/s] = %8.5e\n\nData needed for Woodhouse et al. (2013) model\nAbsolute top plume height [m] = %8.5e\nPlume height-averaged buoyancy frequency [1/s] = %8.5e\nWind speed at top plume height [m/s] = %8.5e\nWs = %8.5e\n' % (
        P_H_source, T_H_source, N_avg, V_avg, H_top, N_avg, V_H_top, Ws))