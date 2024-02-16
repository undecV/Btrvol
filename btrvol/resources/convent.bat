:: https://stackoverflow.com/a/49823738
convert -background transparent "favicon.png" -define icon:auto-resize=16,24,32,48,64,72,96,128,256 "favicon.ico"
convert -background transparent "favicon.png" -define icon:auto-resize=16 "favicon_16.ico"
@pause
