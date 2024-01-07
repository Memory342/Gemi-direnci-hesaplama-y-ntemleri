% Manuel olarak tanımlanan VL, DL ve CR1 array'leri
VL_values = [0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3];
DL_values = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250];
CR1_array = load('cr1.txt'); % Dosya adını ve yolu güncelleyin

% Scatter plot çizimi
figure;
scatter(repelem(VL_values, length(DL_values)), repmat(DL_values, 1, length(VL_values)), 50, CR1_array(:), 'filled');
colorbar;
clim([-1, 10]);
xlabel('VL (x ekseni)');
ylabel('DL (y ekseni)');
title('VL, DL ve CR1 Scatter Plot');
