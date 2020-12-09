
    anchorName = 'foreman69.Y';
    targetName = 'foreman72.Y';
    frameHeight = 352;
    frameWidth = 288;
    blockSize = [16,16];
    fid = fopen(anchorName,'r');
    anchorFrame = fread(fid,[frameHeight,frameWidth]);
    anchorFrame = anchorFrame';
    fclose(fid);
    fid = fopen(targetName,'r');
    targetFrame = fread(fid,[frameHeight,frameWidth]);
    targetFrame = targetFrame';
    fclose(fid);
    tic
    [predictFrame, mv_d, mv_o] = ebma(targetFrame, anchorFrame, blockSize);
    time_ebma=toc;
    errorFrame = imabsdiff(anchorFrame, predictFrame);
    MSE_ebma = zeros(1,33);
    MSE_ebma(16) = mean(mean((errorFrame.^2)));

    % Plots II.1
    figure
    subplot(1,2,1),imshow(uint8(anchorFrame)), title('Frame de referencia');
    subplot(1,2,2),imshow(uint8(targetFrame)), title('Frame objetivo');

    figure, imshow(uint8(anchorFrame))
    hold on
    quiver(mv_o(1,:),mv_o(2,:),mv_d(1,:),mv_d(2,:)), title(sprintf('Vectores de movimiento EBMA %gx%g', i, i));
    hold off
    
        frame1=getframe;
    
    
    figure
    imshow(uint8(predictFrame)), title(sprintf('Frame estimado EBMA %gx%g', 16, 16));
    
        frame2=getframe;
    
    fprintf('MSE EBMA %gx%g:', 16, 16);
    display(MSE_ebma(16));
