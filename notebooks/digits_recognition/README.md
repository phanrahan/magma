# MNIST handwritten digits recognition on IceStick FPGA

## Introduction

This example designs a very simple pipeline for handwritten digits recognition using one-layer binary "neural network". The architecture is output stationary. The image is resized to 16x16, and operand width in execution stage of pipeline is 16 bit. The pipeline contains five stages:

![binary matrix vector multiplication](/notebooks/digits_recognition/images/bmv.png)

- IF: calculate IDX and CYCLE as shown in figure
- RR: read weight matrix and image block from ROM and LUTs
- EXE: using NXOR and Popcount to perform binary matrix multiplication and accumulate results
- CP: compare result to previous maximum result and save the index (prediction number) for maximum result
- FI: wait to show result until all calculation completes

There are five lights (D0, D1, D2, D3, D4) on the IceStick FPGA. The D5 LED is green which indicates the finish of calculation. Others are red and used for indicates binary representation of predited number.

### Directories and Files

`nn_train` contains tutorials of training a binary neural network for digits recognition and format of saving weight matrix and images used for FPGA.

`nn_train/BNN.pkl` contains the weight matrix and images we seleted. Only number 5 is incorrectly recognized as 9 and other numbers can be perfectly recognized.

`test_modules` shows the simulation of our pipeline.

`tutorial_digits_recognition_on_icestick` is the tutorial to convert our code to verilog and download to icestick FPGA for experiments.

## LICENSE

The MIT License
Copyright (c) 2017 Yujun Lin, Kaidi Cao, Song Han
