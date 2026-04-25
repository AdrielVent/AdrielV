% verify_selected_design.m
% Independently verify selected plate-fin design using CSV outputs.

clear; clc;

selected_csv = fullfile('outputs', 'tables', 'selected_plate_fin_design.csv');
passing_csv = fullfile('outputs', 'tables', 'plate_fin_passing_geometries.csv');

fprintf('Reading selected design CSV: %s\n', selected_csv);
selected_tbl = readtable(selected_csv, 'TextType', 'string');

fprintf('Reading passing geometries CSV: %s\n', passing_csv);
passing_tbl = readtable(passing_csv, 'TextType', 'string');

% Convert selected key-value rows into a map-like struct.
param_names = string(selected_tbl.parameter);
param_values = selected_tbl.value;

selected = struct();
for i = 1:height(selected_tbl)
    key = matlab.lang.makeValidName(param_names(i));
    selected.(key) = param_values(i);
end

% Required verification targets.
TARGET_R_TOTAL = 0.405127;
TARGET_T_CHIP = 65.512732;
TARGET_SPACING = 0.0021125;
R_ALLOW = 0.45;
T_DERATED = 70.0;
SPACING_MIN = 0.002;
TOL = 1e-6;

R_total = selected.R_total;
T_chip = selected.T_chip;
spacing = selected.fin_spacing;

checks = {
    'R_total exact match (0.405127 C/W)', abs(R_total - TARGET_R_TOTAL) <= TOL;
    'T_chip exact match (65.512732 C)', abs(T_chip - TARGET_T_CHIP) <= TOL;
    'Spacing exact match (0.0021125 m)', abs(spacing - TARGET_SPACING) <= TOL;
    'R_total <= 0.45 C/W', R_total <= R_ALLOW;
    'T_chip <= 70 C', T_chip <= T_DERATED;
    'Spacing >= 0.002 m', spacing >= SPACING_MIN;
};

fprintf('\n=== Selected Design Verification ===\n');
all_pass = true;
for i = 1:size(checks, 1)
    label = checks{i, 1};
    ok = checks{i, 2};
    if ok
        fprintf('PASS: %s\n', label);
    else
        fprintf('FAIL: %s\n', label);
        all_pass = false;
    end
end

if all_pass
    fprintf('OVERALL: PASS\n');
else
    fprintf('OVERALL: FAIL\n');
end

% Convert needed passing-table columns to numeric.
num_fins = double(passing_tbl.num_fins);
fin_height_m = double(passing_tbl.fin_height_m);
fin_thickness_m = double(passing_tbl.fin_thickness_m);
base_thickness_m = double(passing_tbl.base_thickness_m);
R_total_passing = double(passing_tbl.R_total_K_per_W);
T_chip_passing = double(passing_tbl.T_chip_C);

% Compute mass (kg) from geometry assumptions used in Python sweep.
BASE_LENGTH_M = 0.0508;
BASE_WIDTH_M = 0.0508;
FIN_SPAN_M = 0.0508;
RHO_AL = 2700.0; % kg/m^3

base_volume = BASE_LENGTH_M * BASE_WIDTH_M .* base_thickness_m;
fins_volume = num_fins .* fin_height_m .* fin_thickness_m .* FIN_SPAN_M;
mass_kg = RHO_AL .* (base_volume + fins_volume);

% Ensure report_assets exists for plot outputs.
out_dir = 'report_assets';
if ~exist(out_dir, 'dir')
    mkdir(out_dir);
end

% 1) mass_kg vs R_total_K_per_W
f1 = figure('Color', 'w');
scatter(mass_kg, R_total_passing, 28, 'filled');
hold on;
yline(R_ALLOW, '--r', 'R_{total} target = 0.45 C/W', 'LineWidth', 1.2);
xlabel('Mass (kg)');
ylabel('R_{total} (C/W)');
title('Passing Geometries: Mass vs Total Thermal Resistance');
grid on;
set(gca, 'FontSize', 10);
saveas(f1, fullfile(out_dir, 'matlab_mass_vs_rtotal.png'));

% 2) num_fins vs T_chip_C
f2 = figure('Color', 'w');
scatter(num_fins, T_chip_passing, 28, 'filled');
hold on;
yline(T_DERATED, '--r', 'T_{chip} target = 70 C', 'LineWidth', 1.2);
xlabel('Number of fins');
ylabel('T_{chip} (C)');
title('Passing Geometries: Number of Fins vs Chip Temperature');
grid on;
set(gca, 'FontSize', 10);
saveas(f2, fullfile(out_dir, 'matlab_num_fins_vs_temperature.png'));

% 3) fin_height_m vs T_chip_C
f3 = figure('Color', 'w');
scatter(fin_height_m, T_chip_passing, 28, 'filled');
hold on;
yline(T_DERATED, '--r', 'T_{chip} target = 70 C', 'LineWidth', 1.2);
xlabel('Fin height (m)');
ylabel('T_{chip} (C)');
title('Passing Geometries: Fin Height vs Chip Temperature');
grid on;
set(gca, 'FontSize', 10);
saveas(f3, fullfile(out_dir, 'matlab_fin_height_vs_temperature.png'));

fprintf('\nSaved plots:\n');
fprintf(' - %s\n', fullfile(out_dir, 'matlab_mass_vs_rtotal.png'));
fprintf(' - %s\n', fullfile(out_dir, 'matlab_num_fins_vs_temperature.png'));
fprintf(' - %s\n', fullfile(out_dir, 'matlab_fin_height_vs_temperature.png'));
