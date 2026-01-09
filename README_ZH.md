<div align="center">
  <a href="项目主页链接">
    <img src="awa.gif" alt="Logo" width="320" height="480">
  </a>

  <h1>GPT-SoVITS-RT</h1>

  <p>
    🚀 <b>GPT-SoVITS-RealTime</b> 
    <br>
    A high-performance inference engine specifically designed for the GPT-SoVITS text-to-speech model
  </p>

  <p align="center">
      <a href="LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
      </a>
      <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
      </a>
      <a href="https://github.com/chinokikiss/GPT-SoVITS-RT/stargazers">
        <img src="https://img.shields.io/github/stars/chinokikiss/GPT-SoVITS-RT?style=for-the-badge&color=yellow&logo=github" alt="GitHub stars">
      </a>
  </p>

  <p>
    <a href="README.md">
      <img src="https://img.shields.io/badge/English-66ccff?style=flat-square&logo=github&logoColor=white" alt="English">
    </a>
    &nbsp;
    <a href="README_ZH.md">
      <img src="https://img.shields.io/badge/简体中文-ff99cc?style=flat-square&logo=github&logoColor=white" alt="Chinese">
    </a>
  </p>
</div>

<div align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
</div>

## 前言 (Preface)

本项目诞生的初衷源于对极致性能的追求。我在原版 GPT-SoVITS 的使用过程中，受限于 RTX 3050 (Laptop) 的算力瓶颈，推理延迟往往难以满足实时交互的需求。

为了打破这一限制，**GPT-SoVITS-RT** 应运而生，它是基于 **V2Pro** 模型开发的推理后端。通过一些深度优化技术，本项目成功在低显存环境下实现了毫秒级的实时响应。

除了性能上的飞跃，**GPT-SoVITS-RT** 还加入了音字精准对齐与音频音色迁移等特色功能。

为了便于开发者集成，**GPT-SoVITS-RT** 大幅精简了代码架构，且体积被压缩至 **800MB**。

## 性能对比 (Performance)

> [!NOTE]
> **测试环境**：单卡 NVIDIA GeForce RTX 3050 (Laptop)

| 推理后端 (Backend)| 设置 (Settings) | 首包延迟 (TTFT) | 实时率 (RTF) | 显存 (VRAM) | 提升幅度 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Original** | `streaming_mode=3` | 436 ms | 0.381 | 1.6 GB | - |
| **RT Version** | `Flash_Attn=Off` | 150 ms | 0.125 | **0.8 GB** | ⚡ **2.9x** Speed |
| **RT Version** | `Flash_Attn=On` | **133 ms** | **0.108** | **0.8 GB** | 🔥 **3.3x** Speed |

可以看到，**GPT-SoVITS-RT** 实现了 **3x** 速度提升，且显存占用 **减半**！🚀
<br>

## 环境准备 (Prerequisites)

- **Anaconda**
- **CUDA Toolkit**
- **Microsoft Visual C++**

## 快速开始 (Quick Start)

```bash
conda create -n gsv-rt python=3.11
conda activate gsv-rt
conda install "ffmpeg"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
