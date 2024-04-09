library('TPMplt')


head(TPMdata[,1:3])
TCorrect_data <- TCorrect(TPMdata, 2, 3, 0.9, 7.8, 502.416, seq(0, 0.9, 0.02))
epstable <- epsExtract(TCorrect_data, eps = 0.7, lyT = 2, lySR = 3)
DMM <- DMMprocess(epstable)
PLTbd <- SVRModel(DMM)
print(class(PLTbd))