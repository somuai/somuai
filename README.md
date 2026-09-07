<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:1e293b,100:334155&height=140&section=header&text=Soumyajit%20Ghosh&fontSize=42&fontColor=ffffff&fontAlignY=45" width="100%" alt="Header" />

<a href="https://github.com/somuai">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2800&pause=900&color=38BDF8&center=true&vCenter=true&width=650&height=40&lines=AI+Systems+%26+Distributed+Infrastructure;Core+Contributor+to+Tier-1+Open+Source;Autonomous+Agents+%26+Model+Optimization;Machine+Learning+Tooling+%26+Security" alt="Typing SVG" />
</a>

<p align="center">
  <a href="https://somuai-dev.vercel.app/"><img src="https://img.shields.io/badge/Portfolio-somuai--dev-0284c7?style=flat-square&logo=vercel&logoColor=white" alt="Portfolio" /></a>
  <a href="https://www.linkedin.com/in/soumyajit-ghosh-158b9b285/"><img src="https://img.shields.io/badge/LinkedIn-Soumyajit%20Ghosh-0077b5?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://github.com/somuai"><img src="https://img.shields.io/badge/GitHub-somuai-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="mailto:23051387@kiit.ac.in"><img src="https://img.shields.io/badge/Email-Contact-ea4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
</p>

</div>

---

### Profile Overview

<table>
  <tr>
    <td width="72%" valign="top">
      <p>
        AI Systems Engineer focused on foundation model infrastructure, agentic runtimes, and distributed systems. 
        Active contributor to Tier-1 open-source machine learning frameworks including Hugging Face Transformers, 
        Google DeepMind Optax, Google ADK, and Anthropic Model Context Protocol.
      </p>
      <ul>
        <li><b>Focus Areas</b>: Rotary Position Embeddings (RoPE), Optimizer Numerical Stability, Multi-Agent Orchestration, High-Throughput Inference.</li>
        <li><b>Engineering Philosophy</b>: Deterministic guardrails, zero-allocation memory paths, clean architectural modularity.</li>
        <li><b>Current Work</b>: Autonomous developer agents, AST-based self-healing pipelines, and real-time LLM gateways.</li>
      </ul>
    </td>
    <td width="28%" align="center" valign="middle">
      <img src="assets/avatar.png" width="140" height="140" style="border-radius: 50%; border: 2px solid #38bdf8;" alt="Soumyajit Ghosh" />
      <br />
      <sub><b>Soumyajit Ghosh</b></sub>
      <br />
      <sub>B.Tech, KIIT University</sub>
    </td>
  </tr>
</table>

---

### Tier-1 Open Source Provenance

| Organization / Repository | Focus Area | Contribution Highlights | Pull Request | Status |
| :--- | :--- | :--- | :--- | :--- |
| **PyTorch** (`ao`) | Quantization & Compiler | Handled `aten.abs` and amax-path ops in `Float8TrainingTensor` dispatch under HOP retrace | [#4870](https://github.com/pytorch/ao/pull/4870) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **vLLM** (`vllm`) | Speculative Decoding | Resolved `n_predict` from `text_config` for Qwen3.5 multimodal MTP wrapper checkpoints | [#55369](https://github.com/vllm-project/vllm/pull/55369) | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Hugging Face** (`transformers`) | Trainer & Token Alignment | Prevented `bos_token_id` erasure in `align_special_tokens` for Qwen and Falcon configs | [#48598](https://github.com/huggingface/transformers/pull/48598) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **vLLM** (`vllm`) | Speculative Decoding | Default `num_speculative_tokens` from draft config and defer multi-token warnings | [#55362](https://github.com/vllm-project/vllm/pull/55362) | <img src="https://img.shields.io/badge/Approved-238636?style=flat-square&logo=github&logoColor=white" alt="Approved" /> |
| **vLLM** (`vllm`) | Responses API | Ordered in-flight tool call chunks to prevent stream boundary collapse | [#55371](https://github.com/vllm-project/vllm/pull/55371) | <img src="https://img.shields.io/badge/Approved-238636?style=flat-square&logo=github&logoColor=white" alt="Approved" /> |
| **Keras** (`keras`) | Core API & Ops | Exported `random` submodule and operations under public `keras.ops` namespace | [#23580](https://github.com/keras-team/keras/pull/23580) | <img src="https://img.shields.io/badge/CI_Passed-238636?style=flat-square&logo=githubactions&logoColor=white" alt="CI Passed" /> |
| **Weights & Biases** (`wandb`) | Artifact Subsystem | Bounded auto-generated internal artifact names to 128 chars with middle truncation | [#12755](https://github.com/wandb/wandb/pull/12755) | <img src="https://img.shields.io/badge/CI_Passed-238636?style=flat-square&logo=githubactions&logoColor=white" alt="CI Passed" /> |
| **Google DeepMind** (`optax`) | Numerical Optimization | Prevented NaN divergence in Adam/Adamax optimizers under float16 zero-gradients | [#1768](https://github.com/google-deepmind/optax/pull/1768) | <img src="https://img.shields.io/badge/Resolved-238636?style=flat-square&logo=github&logoColor=white" alt="Resolved" /> |
| **OpenTelemetry** (`opentelemetry-python`) | Distributed Tracing | Built order-independent metric conflict detection on default-view fallback streams | [#5632](https://github.com/open-telemetry/opentelemetry-python/pull/5632) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **OpenContainers** (`runc`) | Container Runtimes | Engineered kernel VFS `/proc` fallback in `FchmodFile` for custom Linux 5.10 kernels | [#5447](https://github.com/opencontainers/runc/pull/5447) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **Containerd** (`containerd`) | Container Engines | Implemented direct upload fallback on cross-repo mount 403 Forbidden responses | [#14118](https://github.com/containerd/containerd/pull/14118) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **SGLang** (`sglang`) | AI Inference | Added multimodal embedding zero-padding guard preventing server SIGQUIT crashes | [#38155](https://github.com/sgl-project/sglang/pull/38155) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **Hugging Face** (`transformers`) | Architecture & Modeling | Validated RoPE dimension parity across heterogeneous model configurations | [#48524](https://github.com/huggingface/transformers/pull/48524) | <img src="https://img.shields.io/badge/In_Review-238636?style=flat-square&logo=githubactions&logoColor=white" alt="In Review" /> |
| **Dokploy** (`dokploy`) | Security & Auth | Enforced server-side SSO boundary across passkey, email, and social sign-in | [#5291](https://github.com/Dokploy/dokploy/pull/5291) | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Dokploy** (`dokploy`) | Cloud Infrastructure | Allowed `+` and `@` in `readValidDirectory` safe path validation | [#5190](https://github.com/Dokploy/dokploy/pull/5190) | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Google** (`adk-go`) | Agent Runtime | Clone Tools and Toolsets slices in constructor to prevent backing array aliasing | [#1493](https://github.com/google/adk-go/pull/1493) | <img src="https://img.shields.io/badge/In_Review-38bdf8?style=flat-square&logo=github&logoColor=white" alt="In Review" /> |
| **Google** (`adk-go`) | Agent Runtime | Added misspell linter, US spelling sweep, and HTTP cassette isolation | [#1465](https://github.com/google/adk-go/pull/1465) | <img src="https://img.shields.io/badge/In_Review-238636?style=flat-square&logo=githubactions&logoColor=white" alt="In Review" /> |
| **Comet ML** (`opik`) | LLM Evaluation Platform | Unit test coverage for `IsJson` metric evaluation | [#8001](https://github.com/comet-ml/opik/pull/8001) | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **First Contributions** (`first-contributions`) | Community Infrastructure | Contributor record and directory onboarding | [#124195](https://github.com/firstcontributions/first-contributions/pull/124195) | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |

---

### Merged Open-Source Contributions (Live Dynamic Feed)

<!-- MERGED_PRS_START -->

| Repository | Contribution Highlight | Pull Request | Merged Date | Status |
| :--- | :--- | :--- | :--- | :--- |
| **vllm-project/vllm** | [Bugfix][Spec Decode] Resolve n_predict from text_config for Qwen3.5 multimodal MTP | [#55369](https://github.com/vllm-project/vllm/pull/55369) | `2026-09-07` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Dokploy/dokploy** | fix(auth): enforce SSO on server-side sign-in endpoints | [#5291](https://github.com/Dokploy/dokploy/pull/5291) | `2026-09-04` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Syknapse/Contribute-To-This-Project** | Add Soumyajit Ghosh card | [#4736](https://github.com/Syknapse/Contribute-To-This-Project/pull/4736) | `2026-09-01` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **firstcontributions/first-contributions** | docs: add Soumyajit Ghosh to contributors list | [#124195](https://github.com/firstcontributions/first-contributions/pull/124195) | `2026-09-01` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Dokploy/dokploy** | fix(server): allow '+' and '@' in readValidDirectory path validation | [#5190](https://github.com/Dokploy/dokploy/pull/5190) | `2026-08-26` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **comet-ml/opik** | test(python-sdk): add unit test coverage for IsJson metric | [#8001](https://github.com/comet-ml/opik/pull/8001) | `2026-08-26` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **lingdojo/kana-dojo** | content: add new japanese proverb | [#29155](https://github.com/lingdojo/kana-dojo/pull/29155) | `2026-08-25` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **lingdojo/kana-dojo** | content: add new japan fact | [#29154](https://github.com/lingdojo/kana-dojo/pull/29154) | `2026-08-25` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **firstcontributions/first-contributions** | Add Soumyajit Ghosh portfolio to Contributors list | [#123556](https://github.com/firstcontributions/first-contributions/pull/123556) | `2026-08-20` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **Syknapse/Contribute-To-This-Project** | Add contributor card for Soumyajit Ghosh | [#4717](https://github.com/Syknapse/Contribute-To-This-Project/pull/4717) | `2026-08-20` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |
| **firstcontributions/first-contributions** | Add Soumyajit Ghosh to Contributors list | [#123511](https://github.com/firstcontributions/first-contributions/pull/123511) | `2026-08-19` | <img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" /> |

<!-- MERGED_PRS_END -->

---

### Tech Stack & Tooling

<div align="left">

#### Languages & Core Runtimes
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=python,go,ts,js,c,cpp,bash" alt="Languages" />
</a>

#### Machine Learning & AI Engineering
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=pytorch,tensorflow,fastapi,huggingface" alt="ML Frameworks" />
</a>

#### Infrastructure, Databases & Cloud
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=docker,postgres,redis,sqlite,gcp,git,githubactions,linux" alt="Infrastructure" />
</a>

#### Frontend & Full-Stack Systems
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=react,nextjs,tailwind,nodejs" alt="Frontend" />
</a>

</div>

---

### Contribution Analytics

<div align="center">
  <img src="https://streak-stats.demolab.com/?user=somuai&theme=tokyonight&hide_border=true&card_width=520" alt="GitHub Contribution Streak" />
</div>

---

### Flagship Projects & Systems

- **[codexmap](https://github.com/somuai/codexmap)**: Real-time self-healing multi-agent cockpit for code generation, AST dependency mapping, and context drift prevention.
- **[clura-v2](https://github.com/somuai/clura-v2)**: Self-hosted OAuth 2.0 and OpenID Connect identity provider built with Bun, Express, Next.js, and PostgreSQL.
- **[Saathi](https://github.com/somuai/Saathi)**: AI grief companion architecture featuring low-latency multimodal video and real-time session recovery.
- **[parity](https://github.com/somuai/parity)**: Automated financial reconciliation engine detecting transactional anomalies across frozen bank statements and internal ledgers.

---

### Contact & Collaboration

- LinkedIn: [Soumyajit Ghosh](https://www.linkedin.com/in/soumyajit-ghosh-158b9b285/)
- Portfolio: [somuai-dev.vercel.app](https://somuai-dev.vercel.app/)
- GitHub: [@somuai](https://github.com/somuai)
- Email: [23051387@kiit.ac.in](mailto:23051387@kiit.ac.in)
- Open to collaboration on foundation model inference kernels, distributed agent orchestration, and open-source infrastructure.
