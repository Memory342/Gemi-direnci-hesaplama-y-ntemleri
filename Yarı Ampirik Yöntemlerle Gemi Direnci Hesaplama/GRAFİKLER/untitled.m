% Veri örnekleri
uzunluk = [46.56;53.76;54;60.96;61.2;61.44;68.16;68.4;68.64;68.88;69.12;75.6;75.84;76.08;76.32;83.04;83.28;83.52;90.48;90.72];
genislik = [7.69;7.69;8.79;7.69;8.79;9.97;7.69;8.79;9.97;10.96;12.04;8.79;9.97;10.96;12.04;9.97;10.96;12.04;10.96;12.04];
su_cekimi = [2.8;2.8;3.0;2.8;3.0;3.2;2.8;3.0;3.2;3.4;3.6;3;3.2;3.4;3.6;3.2;3.4;3.6;3.4;3.6];
deplasman_hacmi = [442;507;649;577;738;895;681;817;999;1204;1400;950;1105;1334;1553;1270;1450;1690;1650;1927];

% Scatter plot
figure;
scatter3(uzunluk, genislik, su_cekimi, 50, deplasman_hacmi, 'filled');
xlabel('Uzunluk');
ylabel('Genişlik');
zlabel('Su Çekimi');
title('Scatter Plot');

% Regresyon
X = [uzunluk, genislik, su_cekimi];
y = deplasman_hacmi;

mdl = fitrgp(X, y, 'FitMethod', 'exact', 'OptimizeHyperparameters', 'auto');

% Yüzey oluşturma
[Xq, Yq, Zq] = meshgrid(linspace(min(uzunluk), max(uzunluk), 100), ...
                        linspace(min(genislik), max(genislik), 100), ...
                        linspace(min(su_cekimi), max(su_cekimi), 100));

queryPoints = [Xq(:), Yq(:), Zq(:)];
deplasman_hacmi_pred = predict(mdl, queryPoints);

% Yüzey çizimi
figure;
scatter3(Xq(:), Yq(:), Zq(:), 50, deplasman_hacmi_pred, 'filled');
xlabel('Uzunluk');
ylabel('Genişlik');
zlabel('Su Çekimi');
title('4 Boyutlu Renkli Yüzey');

