clear all, close all, clc;
file_name = 'shopping_center.mpg';
my_movie = VideoReader(file_name);
vidWidth = my_movie.Width;
vidHeight = my_movie.Height;
mov = struct('cdata',zeros(vidHeight,vidWidth,3,'uint8'),'colormap',[]);
k=1;
while hasFrame(my_movie)
    mov(k).cdata=readFrame(my_movie);
    k=k+1;
end

%Preasignar array de 4D que contendrá todos los frames 
image_data=uint8(zeros(vidHeight, vidWidth,3,my_movie.FrameRate*my_movie.Duration));
for k = 1:my_movie.FrameRate*my_movie.Duration
    image_data(:,:,:,k) = mov(k).cdata;
end

figure
montage(image_data);
