# ReDetGraphTracker

A end-to-end model for Active regions tracking:
![](file:///G:/work/visio_map/FairMOT%E6%94%B9%E8%BF%9B.png)

## Abstract

Solar active regions serve as the primary energy sources of various  solar activities, directly impacting the terrestrial environment. Therefore, precise  detection and tracking of active regions are crucial for space weather monitoring  and forecasting. In this study, a total of 4,532 HMI and MDI longitudinal  magnetograms are selected for building the dataset, including the training  set, validating set, and eight testing sets. They represent different observation  instruments, different numbers of activity regions, and different time intervals. A  new deep learning method, ReDetGraphTracker, is proposed for detecting and  tracking the active regions in full-disk magnetograms. The cooperative modules, especially the re-detection module, NSA Kalman filter, and the splitter module,  better solve the problems of missing detection, discontinuous trajectory, drifting  tracking bounding box, and ID change. The evaluation metrics, IDF1, MOTA,  MOTP, IDs, and FPS, for the testing sets with 24h interval on average are  74.3%, 75.0%, 0.130, 14.5, and 13.7, respectively. With the decreasing intervals,  the metrics become better and better. The experimental results show that  ReDetGraphTracker has a good performance in detecting and tracking active  regions, especially capturing an active region as early as possible and terminating  tracking in real-time. It can well deal with the active regions whatever evolve drastically or with weak magnetic field strengths

## Tracking performance

### Results on AR tracking test set

| Dataset                        | IDF1  | MOTA  | MOTP  | IDs | FPS  |
| ------------------------------ | ----- | ----- | ----- | --- | ---- |
| 2010.07.01-2010.07.31@24h(MDI) | 75.4% | 75.3% | 0.128 | 16  | 13.6 |
| 2000.07.12-2000.08.13@24h(MDI) | 73.2% | 74.1% | 0.130 | 14  | 14.0 |
| 2010.07.01-2010.07.31@24h(HMI) | 76.5% | 77.4% | 0.124 | 16  | 13.8 |
| 2010.11.05-2010.12.04@24h(HMI) | 73.1% | 74.1% | 0.132 | 11  | 13.2 |
| 2024.03.01-2010.05.15@24h(HMI) | 73.4% | 73.8% | 0.129 | 13  | 13.3 |
| 2014.10.01-2014.10.31@24h(HMI) | 72.1% | 73.2% | 0.137 | 12  | 13.4 |
| 2014.10.01-2014.10.31@6h(HMI)  | 82.5% | 87.3% | 0.120 | 11  | 13.2 |
| 2014.10.01-2014.10.31@1h(HMI)  | 86.5% | 88.3% | 0.113 | 8   | 13.1 |
| 2014.10.01-2014.10.31@12m(HMI) | 88.3% | 91.2% | 0.102 | 3   | 13.3 |
| 2014.10.01-2014.10.31@48h(HMI) | 60.4% | 57.3% | 0.234 | 58  | 13.5 |

  The tracking speed of the entire system can reach up to **13 FPS**.



## Installation

* Clone this repo, and we'll call the directory that you cloned as ${ROOT}

* Install dependencies. We use python 3.8 and pytorch >= 1.7.0
  
  ```
  conda create -n ReDetGraphTracker
  conda activate ReDetGraphTracker
  conda install pytorch==1.7.0 torchvision==0.8.0 cudatoolkit=10.2 -c pytorch
  cd ${ROOT}
  pip install cython
  pip install -r requirements.txt
  ```

* We use [DCNv2_pytorch_1.7](https://github.com/ifzhang/DCNv2/tree/pytorch_1.7) in our backbone network (pytorch_1.7 branch). Previous versions can be found in [DCNv2](https://github.com/CharlesShang/DCNv2).
  
  ```
  git clone -b pytorch_1.7 https://github.com/ifzhang/DCNv2.git
  cd DCNv2
  ./make.sh
  ```

* In order to run the code for demos, you also need to install [ffmpeg](https://www.ffmpeg.org/).

## Data preparation

* **Dataset**
  This work employs the full-disk 720-second line-of-sight magnetic field  maps (hmi.M_720s) from the Helioseismic and Magnetic Imager (HMI, Scherrer et al., 2012) on the Solar Dynamics Observatory (SDO) and the full disk  96-minute line-of-sight magnetograms (mdi.fd_M_96m_lev182) from  the Michelson Doppler Image (MDI, Turmon, Pap, and Mukhtar, 2002) on the  Solar and Heliospheric Observatory (SOHO). The training data are all from HMI.  The MDI data are adopted into the test set for verifying the generalization of the method. After downloading, you should prepare the data in the following structure:
  
  ```
  RS-VOC
   |——————images
   |        └——————train
   |                 └——————ARC-image_1
   |                 └——————ARC-image_2
   |                 └——————ARC-image_3
   |                 └——————ARC-image_4
   |        └——————test
   |                 └——————ARC-image_1
   |                 └——————ARC-image_2
   |                 └——————ARC-image_3
   |                 └——————ARC-image_4
   |        └——————val
   |                 └——————ARC-image_1
   |                 └——————ARC-image_2
   |                 └——————ARC-image_3
   |                 └——————ARC-image_4
   └——————labels_with_ids
   |         └——————train(empty)
   |         └——————val(empty)
  
  ```

* Then, you can change the seq_root and label_root in src/gen_labels_15.py and src/gen_labels_20.py and run:
  
  ```
  cd src
  python gen_labels_15.py
  python gen_labels_20.py
  ```
  
  to generate the labels of the dataset. 

## Pretrained models and baseline model

* **Model**

Our best model  is trained  for 200 epochs with the self-supervised learning which will spend 46 hours to train.
After training, you should set the path to put the trained model in the following structure:

```
${ROOT}
   └——————models
           └——————model_{epoch}.pth
           └——————...
```

## Training

* Set the training data

* Change the dataset root directory 'root' in src/lib/cfg/data.json and 'data_dir' in src/lib/opts.py

* Start train:
  
  ```
  sh experiments/ARC_train.sh
  ```
- You can change settings as:
  
  ```
  python train.py mot --exp_id ARC_train --load_model '' --arch 'base_detection' --NSA --num_epochs 200 --multi_loss 'fix' --lr_step '15' --batch_size 8 --data_cfg '../src/lib/cfg/ARC.json'
  ```
  
  --exp_id is the path of the training result.
  --load_model is a parameter that controls whether to load the pretrained model.
  --arch is the backbone. And you can modify all the parameters in src/lib/opts.py

## Tracking

* The default settings run tracking on the validation dataset . Using the best model, you can run:
  
  ```
  cd src
  python track.py mot --load_model ../exp/mot/ARC_tain/model_last.pth --conf_thres 0.6
  ```
  
   You can also set save_images=True in src/track.py to save the visualization results of each frame. 

* To get the txt results of the test set , you can run:
  
  ```
  cd src
  python track.py mot --test_ARC True --load_model ../models/model_last.pth --conf_thres 0.4
  ```

## Demo

You can input a raw images and get the demo output by running src/demo.py and get the result format of the demo:

```
cd src
python demo.py mot --load_model ../models/model_last.pth --conf_thres 0.4
```

You can change --inpu and --output-root to get the demos of your own images.
--conf_thres can be set from 0.3 to 0.7 depending on your own input.




