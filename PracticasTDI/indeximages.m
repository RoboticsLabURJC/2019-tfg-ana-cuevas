lena = imread('lena.jpg');

lenagray = rgb2gray(lena);

%imtool(lena);

[lenaind256, map256] = rgb2ind(lena, 256);


%figure
%title('255');
%imtool(lenaind256);

[lenaind5, map5] = rgb2ind(lena, 5);

imshow(lenaind5, map5)
%imtool(lenaind5);

[lenagray5, mapgray5] = gray2ind(lenagray, 5);

clear lena lenagray;

save('map255.mat', '-v7');
