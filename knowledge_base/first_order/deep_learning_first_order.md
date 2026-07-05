# First Order: Deep Learning
**Authors:** Ian Goodfellow, Yoshua Bengio, Aaron Courville  
**Processed:** 2026-07-01  
**Total Chapters:** 20 (plus Introduction)  
**Publisher:** MIT Press, 2016

---

## Chapter 1: Introduction

### Core Argument
Deep learning solves the problem of getting computers to understand intuitive, informal knowledge by learning hierarchical representations from data, where each level of the hierarchy builds on simpler concepts from the level below.

### Key Concepts & Algorithms

**Machine Learning:** The ability of AI systems to acquire their own knowledge by extracting patterns from raw data, rather than relying on hard-coded rules. Allows computers to tackle problems involving knowledge of the real world.

**Representation Learning:** Using machine learning to discover not just the mapping from representation to output, but also the representation itself. Learned representations often outperform hand-designed ones and allow rapid adaptation to new tasks.

**Deep Learning:** A particular kind of machine learning that achieves power by learning to represent the world as a nested hierarchy of concepts. Each concept is defined in relation to simpler concepts. The depth refers to the length of the longest path through the computational graph.

**Multilayer Perceptron (MLP) / Feedforward Deep Network:** The quintessential deep learning model. A mathematical function mapping input values to output values, formed by composing many simpler functions. Each function application provides a new representation of the input.

**Autoencoder:** A representation learning algorithm combining an encoder (converts input to different representation) and a decoder (converts representation back to original format). Different autoencoders aim to achieve different properties of the learned representation.

**Factors of Variation:** Sources of influence that explain the observed data. Deep learning aims to disentangle these factors. Examples: in a car image, position, color, viewing angle, lighting.

**Historical Waves of Deep Learning:**
- Wave 1 (1940s–1960s): Cybernetics. McCulloch-Pitts Neuron (1943), Hebb's learning rule (1949), Perceptron (Rosenblatt, 1958), ADALINE (Widrow and Hoff, 1960).
- Wave 2 (1980s–1990s): Connectionism / Parallel Distributed Processing. Back-propagation (Rumelhart et al., 1986), LSTM (Hochreiter and Schmidhuber, 1997).
- Wave 3 (2006–present): Deep learning. Hinton et al. (2006), Bengio et al. (2007). Resurgence driven by larger datasets, more compute, and algorithmic improvements.

**Distributed Representation (Hinton et al., 1986):** Each input should be represented by many features, and each feature should be involved in the representation of many inputs. Exponentially more efficient than local representations.

**Key Historical Result:** IBM Deep Blue defeated world chess champion Garry Kasparov in 1997. Demonstrates that formal rule-based problems were already solved; the hard problems were intuitive ones.

**Network Scale:** Neural networks have grown exponentially for three decades. As of 2016, artificial neural networks are only as large as the nervous systems of insects.

**Neural Scale Law (empirical):** Network size approximately doubles every 2.4 years. In 2016, networks had roughly 10^7–10^9 parameters.

### Key Results & Benchmarks
- Ferret cortex rewiring experiment (Von Melchner et al., 2000): Ferrets can learn to see with auditory cortex when visual signals are rerouted there, suggesting a single general learning algorithm may underlie most brain function.
- Perceptron proved unable to learn XOR function (Minsky and Papert, 1969) — key limitation of linear models.

### Logical Structure
Chapter 1 establishes the motivation for deep learning by contrasting it with rule-based AI (Cyc) and simple ML (logistic regression). It introduces the core idea that learning hierarchical representations enables computers to understand intuitive knowledge. The chapter traces three historical waves and sets up the book's three-part structure.

### Notable Quotes
> "Deep learning is a particular kind of machine learning that achieves great power and flexibility by learning to represent the world as a nested hierarchy of concepts, with each concept defined in relation to simpler concepts." — p.1

> "Machine learning is the only viable approach to building AI systems that can operate in complicated, real-world environments." — p.8

### Cross-Chapter Connections
Prerequisite to all chapters. Chapter 5 extends ML basics. Chapters 6-10 implement the core deep learning ideas introduced here. Chapter 15 develops representation learning fully.

---

## Chapter 2: Linear Algebra

### Core Argument
A core subset of linear algebra concepts — scalars, vectors, matrices, eigendecomposition, SVD, norms, and PCA — provides the mathematical language for understanding deep learning operations.

### Key Concepts & Algorithms

**Scalars, Vectors, Matrices, Tensors:** Fundamental data containers. Scalars (single numbers), vectors (1D arrays), matrices (2D arrays), tensors (N-D arrays). Deep learning operates primarily on tensors.

**Matrix Multiplication:** For $C = AB$, $C_{i,j} = \sum_k A_{i,k} B_{k,j}$. Matrix products are distributive and associative but generally not commutative.

**Hadamard (Element-wise) Product:** $A \odot B$, element-wise multiplication. Distinct from matrix multiplication.

**Identity and Inverse Matrices:** $I_n$ has 1s on diagonal, 0s elsewhere. $A^{-1}A = I$. The matrix inverse allows solving $Ax = b$ as $x = A^{-1}b$, though numerically this is often done via Gaussian elimination.

**Norms:** Measure the size of a vector. $L^p$ norm: $\|x\|_p = (\sum_i |x_i|^p)^{1/p}$.
- $L^2$ (Euclidean) norm: most common in ML
- $L^1$ norm: preferred when zero vs. non-zero matters (promotes sparsity)
- $L^\infty$ (max) norm: absolute value of the largest element
- Frobenius norm (for matrices): $\|A\|_F = \sqrt{\sum_{i,j} A_{i,j}^2}$, analogous to $L^2$ norm

**Eigendecomposition:** $A = V \text{diag}(\lambda) V^{-1}$, where columns of $V$ are eigenvectors and $\lambda$ contains eigenvalues. Every real symmetric matrix can be decomposed as $A = Q \Lambda Q^\top$ where $Q$ is orthogonal. A matrix is positive definite (all eigenvalues > 0), positive semidefinite (all ≥ 0), negative definite (all < 0), or indefinite (mixed).

**Singular Value Decomposition (SVD):** $A = UDV^\top$ where $U$ and $V$ are orthogonal matrices, $D$ is diagonal (singular values). More general than eigendecomposition — works for non-square matrices. Singular values are related to eigenvalues of $A^\top A$.

**Moore-Penrose Pseudoinverse:** $A^+ = V D^+ U^\top$ where $D^+$ inverts nonzero diagonal elements. Provides a solution to $Ax = y$ even when $A$ is not square or is singular. Minimizes $\|Ax - y\|_2$ when multiple solutions exist.

**Trace Operator:** $\text{Tr}(A) = \sum_i A_{i,i}$. Invariant under cyclic permutation: $\text{Tr}(ABC) = \text{Tr}(CAB) = \text{Tr}(BCA)$.

**Determinant:** $\det(A)$ — product of all eigenvalues. Measures how much the matrix expands or contracts space. Zero determinant means the matrix is singular (non-invertible).

**Principal Components Analysis (PCA):** Finds the optimal compressed representation by projecting data onto the directions of maximum variance. The encoder $f(x) = D^\top x$ and decoder $r(x) = DD^\top x$ where $D$ columns are leading eigenvectors of the covariance matrix. Minimizes $L^2$ reconstruction error.

### Logical Structure
Chapter 2 builds the mathematical vocabulary needed for understanding neural network computations. Matrix operations describe layer computations. Eigendecomposition and SVD appear in analysis of optimization (Hessian analysis in Chapter 8) and in understanding weight spaces. PCA is the first concrete learning algorithm, previewing Chapter 13's linear factor models.

### Cross-Chapter Connections
Foundation for all subsequent mathematics. Eigendecomposition critical for understanding Chapter 8 (optimization challenges). SVD appears in Chapter 13 (linear factor models). PCA is a special case of autoencoders (Chapter 14).

---

## Chapter 3: Probability and Information Theory

### Core Argument
Probability theory provides the framework for reasoning under uncertainty, and information theory quantifies the amount of information in distributions — both are essential for understanding deep learning as learning probability distributions over data.

### Key Concepts & Algorithms

**Why Probability in ML:** Two sources of uncertainty in AI: randomness in the system being modeled, and incomplete observability. Even deterministic systems with unobserved causes are best modeled probabilistically.

**Probability Distributions:** Functions describing how probable different outcomes are.
- Discrete: probability mass function (PMF) $P(x)$, satisfies $\sum_x P(x) = 1$
- Continuous: probability density function (PDF) $p(x)$, satisfies $\int p(x)dx = 1$

**Joint Probability:** $P(x, y)$, probability that both $x$ and $y$ occur simultaneously.

**Marginal Probability:** $P(x) = \sum_y P(x, y)$ (discrete) or $p(x) = \int p(x, y)dy$ (continuous).

**Conditional Probability:** $P(y | x) = P(x, y) / P(x)$, probability of $y$ given $x$.

**Chain Rule:** $P(x^{(1)}, ..., x^{(n)}) = \prod_{i=1}^{n} P(x^{(i)} | x^{(1)}, ..., x^{(i-1)})$.

**Independence:** $x \perp y$ iff $P(x, y) = P(x)P(y)$. Conditional independence: $x \perp y | z$ iff $P(x, y | z) = P(x|z)P(y|z)$.

**Expectation, Variance, Covariance:**
- $E[f(x)] = \sum_x P(x) f(x)$ (discrete)
- $\text{Var}(f(x)) = E[(f(x) - E[f(x)])^2]$
- $\text{Cov}(f(x), g(y)) = E[(f(x) - E[f(x)])(g(y) - E[g(y)])]$

**Common Distributions:**
- **Bernoulli:** Binary variable with parameter $\phi \in [0,1]$. $P(x=1)=\phi$, $P(x=0) = 1 - \phi$
- **Multinoulli (Categorical):** Distribution over $k$ categories
- **Gaussian:** $\mathcal{N}(x;\mu,\sigma^2) = \sqrt{\frac{1}{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$. Multivariate: $\mathcal{N}(x;\mu,\Sigma) = \frac{1}{\sqrt{(2\pi)^n \det(\Sigma)}} \exp\left(-\frac{1}{2}(x-\mu)^\top\Sigma^{-1}(x-\mu)\right)$
- **Exponential:** $p(x;\lambda) = \lambda \mathbf{1}_{x \geq 0} \exp(-\lambda x)$. Sharp point at $x=0$
- **Laplace:** $\text{Laplace}(x;\mu,\gamma) = \frac{1}{2\gamma}\exp\left(-\frac{|x-\mu|}{\gamma}\right)$
- **Empirical:** $\hat{p}(x) = \frac{1}{m}\sum_{i=1}^m \delta(x - x^{(i)})$

**Logistic Sigmoid:** $\sigma(x) = \frac{1}{1 + \exp(-x)}$. Range $(0,1)$. Saturates to 0 and 1 at extremes. $\sigma'(x) = \sigma(x)(1-\sigma(x))$.

**Softplus Function:** $\zeta(x) = \log(1 + \exp(x))$. Smooth approximation of $\max(0,x)$. $\zeta'(x) = \sigma(x)$.

**Bayes' Rule:** $P(x | y) = P(x)P(y|x) / P(y)$, where $P(y) = \sum_x P(y|x)P(x)$.

**Shannon Entropy:** $H(x) = -E_x[\log P(x)] = -\sum_x P(x)\log P(x)$. Measures expected amount of information in a distribution. Higher entropy = more uncertainty.

**KL Divergence:** $D_{KL}(P \| Q) = E_x\left[\log\frac{P(x)}{Q(x)}\right] = \sum_x P(x)\log\frac{P(x)}{Q(x)}$. Measures how different distribution $P$ is from $Q$. Not symmetric. Always $\geq 0$, equals 0 iff $P = Q$.

**Cross-Entropy:** $H(P, Q) = H(P) + D_{KL}(P \| Q) = -E_x[\log Q(x)]$. Minimizing cross-entropy with respect to $Q$ (model) is equivalent to minimizing KL divergence from data distribution $P$ to $Q$.

**Structured Probabilistic Models (Graphical Models):** Use directed or undirected graphs to represent conditional independence structure in probability distributions. Enables factorizing a high-dimensional joint distribution into lower-dimensional factors.
- **Directed models (Bayesian networks):** Edges represent conditional probability distributions $P(x | \text{parents}(x))$
- **Undirected models (Markov Random Fields):** Edges represent compatibility functions (factors). Joint distribution is product of factors divided by partition function $Z$.

### Logical Structure
Probability foundations enable maximum likelihood training (Chapter 5), cost function design (Chapter 6), Bayesian regularization approaches (Chapter 7), and all of Part III's generative models.

### Cross-Chapter Connections
Prerequisite to Chapter 4 (numerical computation with probabilities), Chapter 5 (MLE), Chapter 6 (cost functions), and all of Part III (generative models, Chapters 16-20).

---

## Chapter 4: Numerical Computation

### Core Argument
Practical implementation of mathematical operations on computers requires handling numerical issues including overflow, underflow, and ill-conditioning, and understanding gradient-based optimization as the mechanism for training deep networks.

### Key Concepts & Algorithms

**Overflow and Underflow:** Fundamental numerical issues on digital computers.
- **Underflow:** Numbers near zero rounded to zero. Can cause division by zero or log of zero.
- **Overflow:** Very large numbers approximated as infinity.
- **Softmax stabilization:** $\text{softmax}(z)_i = \frac{\exp(z_i)}{\sum_j \exp(z_j)}$. Numerically stable by computing $\text{softmax}(z - \max_j z_j)$.

**Poor Conditioning:** The condition number of a matrix ($\kappa(A) = |\lambda_{max}|/|\lambda_{min}|$) measures how much output change results from small input changes. High condition number means the matrix amplifies errors. Critical for neural network optimization.

**Gradient Descent:** Minimizes a function $f(x)$ by moving in the direction of the negative gradient. Update: $x' = x - \epsilon \nabla_x f(x)$ where $\epsilon$ is the learning rate (step size). Works when the function is locally well-approximated by a linear function.

**Critical Points:** Points where $\nabla_x f(x) = 0$. Can be minima (positive definite Hessian), maxima (negative definite Hessian), or saddle points (indefinite Hessian).

**Gradient, Jacobian, Hessian:**
- Gradient $\nabla_x f(x)$: vector of partial derivatives
- Jacobian $J \in \mathbb{R}^{m \times n}$ of $f: \mathbb{R}^n \to \mathbb{R}^m$: $J_{i,j} = \partial f(x)_i / \partial x_j$
- Hessian $H(f)(x) = \nabla^2_x f(x)$: matrix of second derivatives. $H_{i,j} = \partial^2 f / \partial x_i \partial x_j$

**Second-Order Taylor Expansion:** $f(x) \approx f(x^{(0)}) + (x - x^{(0)})^\top g + \frac{1}{2}(x-x^{(0)})^\top H (x-x^{(0)})$ where $g$ is the gradient and $H$ is the Hessian. Used to analyze learning step size.

**Optimal Step Size:** For a quadratic function, gradient descent with step $\epsilon^* = 1/(g^\top H g) \cdot g^\top g$ gives optimal improvement.

**Newton's Method:** Uses second-order information. Update: $x^* = x_0 - H^{-1}\nabla_x f(x_0)$. Jumps directly to minimum of locally quadratic approximation. Limited by cost of computing and inverting Hessian (scales as $O(n^3)$ for $n$ parameters), and by presence of saddle points where Newton's method can move in the wrong direction.

**Constrained Optimization:** KKT conditions generalize Lagrangian to handle inequality constraints. For $\min f(x)$ subject to $g^{(i)}(x) = 0$ and $h^{(j)}(x) \leq 0$: Lagrangian $\mathcal{L}(x, \lambda, \mu) = f(x) + \sum_i \lambda_i g^{(i)}(x) + \sum_j \mu_j h^{(j)}(x)$.

**Moore-Penrose Pseudoinverse for Linear Least Squares:** Minimizes $\|Ax - b\|_2$ as $x^* = A^+ b$.

### Logical Structure
Chapter 4 bridges the gap between mathematical concepts and practical computation. The optimization foundations (gradient descent, Newton's method, Hessians) are directly applied in Chapter 8. Numerical stability considerations affect implementation of every activation function and cost function in Chapters 6-7.

### Cross-Chapter Connections
Gradient-based optimization (section 4.3) is foundational to all of Part II. The Hessian analysis here previews Chapter 8's detailed treatment of optimization challenges.

---

## Chapter 5: Machine Learning Basics

### Core Argument
Machine learning algorithms learn from data to improve performance on tasks, governed by the tradeoff between underfitting and overfitting — captured through capacity, bias, and variance — with generalization as the ultimate goal.

### Key Concepts & Algorithms

**Learning Algorithm Definition (Mitchell, 1997):** A computer program that learns from experience $E$ with respect to some task $T$ and performance measure $P$, if its performance at $T$ as measured by $P$ improves with experience $E$.

**Tasks Types:** Classification, regression, transcription, machine translation, structured output, anomaly detection, synthesis, missing value imputation, denoising, density estimation.

**Performance Measures:** Accuracy (classification), error rate, log-likelihood, cross-entropy between model and data distribution.

**Training Set, Validation Set, Test Set:** Training data used to optimize parameters. Validation data used to select hyperparameters (choose model). Test data used for unbiased evaluation. Never adjust parameters based on test set.

**Generalization:** Ability to perform well on new, previously unseen data. Key distinction from pure optimization.

**Underfitting vs. Overfitting:**
- Underfitting: model can't achieve sufficiently low error on training set. Model has insufficient capacity.
- Overfitting: large gap between training error and test error. Model too complex for amount of data.

**Capacity:** A model's ability to fit a wide variety of functions. Can be controlled by choosing hypothesis space. Vapnik-Chervonenkis (VC) dimension is a measure of capacity for binary classifiers.

**Bias-Variance Tradeoff:**
- Bias: expected deviation from true value (underfitting)
- Variance: variability of prediction for given input across different training sets (overfitting)
- Mean squared error = Bias$^2$ + Variance + irreducible noise

**No Free Lunch Theorem (Wolpert, 1996):** Averaged over all possible data-generating distributions, every classification algorithm has the same error rate on unobserved points. Must make assumptions (inductive bias) about the data.

**Regularization:** Any modification to a learning algorithm intended to reduce generalization error but not training error. Expresses preference for simpler models. Example: weight decay (L2 regularization) adds $\lambda \|w\|_2^2$ to objective.

**Hyperparameters and Validation Sets:** Hyperparameters not learned by the training algorithm itself (e.g., number of layers, regularization strength). Must be selected using validation set, not test set.

**Estimators, Bias, and Variance:**
- Estimator $\hat{\theta}_m$: any function of the data that provides a guess of $\theta$
- Bias: $\text{bias}(\hat{\theta}_m) = E[\hat{\theta}_m] - \theta$
- Variance: $\text{Var}(\hat{\theta})$
- Standard error: $\text{SE}(\hat{\mu}_m) = \sigma/\sqrt{m}$
- Consistency: $\text{plim}_{m\to\infty} \hat{\theta}_m = \theta$

**Maximum Likelihood Estimation (MLE):** Choose parameters $\theta$ to maximize probability of observed data: $\theta_{ML} = \arg\max_\theta \prod_{i=1}^m p_{model}(x^{(i)};\theta) = \arg\max_\theta \sum_{i=1}^m \log p_{model}(x^{(i)};\theta)$. Equivalent to minimizing KL divergence between empirical data distribution and model distribution.

**Bayesian Statistics:** Uses prior probability distribution $p(\theta)$ over parameters, updated by likelihood to get posterior $p(\theta | x^{(1)},...,x^{(m)}) \propto p(x^{(1)},...,x^{(m)} | \theta) p(\theta)$. Makes predictions by integrating over all parameter values (vs. MLE's point estimate).

**Maximum A Posteriori (MAP):** $\theta_{MAP} = \arg\max_\theta \log p(\theta | x) = \arg\max_\theta [\log p(x|\theta) + \log p(\theta)]$. Point estimate incorporating prior. Using Gaussian prior on parameters gives same result as L2 weight decay.

**Supervised Learning Algorithms:**
- **Logistic Regression:** Predicts $P(y=1|x) = \sigma(\theta^\top x)$. Binary classification.
- **Support Vector Machines:** Finds maximum margin hyperplane separating classes. Kernel trick allows nonlinear boundaries. No probabilistic output.
- **Decision Trees:** Recursive binary partitioning. Each leaf assigns a class.
- **k-Nearest Neighbors:** Classifies based on majority class among k nearest training examples. Nonparametric. Curse of dimensionality limits effectiveness in high dimensions.
- **Kernel Regression:** $f(x) = \sum_i k(x, x^{(i)}) y^{(i)}$. Uses kernel function to measure similarity.

**Unsupervised Learning Algorithms:**
- **PCA:** Finds low-dimensional linear manifold explaining data variance
- **k-Means Clustering:** Partitions data into k clusters minimizing within-cluster variance
- **Gaussian Mixture Models:** Weighted mixture of Gaussians, trained with EM

**Stochastic Gradient Descent (SGD):** Key insight: gradient is an expectation, and can be estimated from a small minibatch. Update using gradient computed on minibatch of $m'$ examples. Enables learning from huge datasets. Convergence conditions: $\sum_k \epsilon_k = \infty$ and $\sum_k \epsilon_k^2 < \infty$.

**Curse of Dimensionality:** Many problems become exponentially harder in high-dimensional spaces. Number of distinct configurations grows exponentially with dimension. Nearest neighbor methods require exponentially more data.

**Manifold Hypothesis:** Real-world data (images, audio, text) lies near a low-dimensional manifold embedded in a high-dimensional space. Deep learning exploits this.

**Challenges Motivating Deep Learning:**
1. Local constancy (smoothness) prior is insufficient for high-dimensional data — requires exponentially many training examples to represent exponentially many regions
2. Deep architectures allow efficient representation through composition

### Key Results & Benchmarks
- Bias-variance tradeoff: at optimal capacity, test error = bias² + variance + noise
- SGD convergence: excess error $O(1/\sqrt{k})$ for convex problems after $k$ steps

### Logical Structure
Chapter 5 establishes the learning framework. Every design decision in Part II (cost functions, regularization, optimization, architectures) addresses one of the challenges identified here. The manifold hypothesis motivates deep networks.

### Cross-Chapter Connections
MLE (section 5.5) is used throughout Part II for cost function design (Ch 6). Regularization (section 5.2) is greatly expanded in Chapter 7. SGD (section 5.9) is the subject of Chapter 8. All of Part III addresses unsupervised learning and generative models.

---

## Chapter 6: Deep Feedforward Networks

### Core Argument
Deep feedforward networks (multilayer perceptrons) are the fundamental architecture of deep learning, trained by gradient descent using back-propagation; their power stems from learning nonlinear feature representations through compositions of parameterized transformations.

### Key Concepts & Algorithms

**Feedforward Network:** Defines a mapping $y = f(x; \theta)$ by composing multiple layers $f(x) = f^{(l)}(f^{(l-1)}(...f^{(1)}(x)...))$. No feedback connections. Training: drive $f(x)$ to match unknown $f^*(x)$.

**Hidden Layers:** Layers not directly specified by training data. The network must decide what each hidden layer computes. Network depth = number of layers (length of chain). Width = dimensionality of hidden layers.

**Activation Functions:** Nonlinear functions applied element-wise to linear transformations. Essential because composing linear functions yields another linear function.

- **ReLU (Rectified Linear Unit):** $g(z) = \max\{0, z\}$ (Jarrett et al., 2009; Nair and Hinton, 2010; Glorot et al., 2011). Current default recommendation. Nearly linear, preserves gradient properties, simple to compute. Drawback: "dying ReLU" — units with negative pre-activations have zero gradient.
  
- **Sigmoid:** $\sigma(z) = 1/(1+\exp(-z))$. Range (0,1). Saturates to 0 and 1. Gradients vanish at extremes. Used for output units, not generally recommended for hidden units.
  
- **Hyperbolic Tangent (tanh):** $g(z) = \tanh(z)$. Range (-1,1). Saturates similarly to sigmoid. Performs better than sigmoid for hidden units due to symmetry around zero.
  
- **Leaky ReLU:** $g(z) = \max\{\alpha z, z\}$ with small $\alpha$ (e.g., 0.01). Allows small gradient when unit is inactive.
  
- **Maxout Units:** $g_i(z) = \max_{j \in [k]} z_{i,j}$. Takes max of $k$ linear functions. Can approximate any convex function. Doubles (or more) parameter count.
  
- **Softmax:** $\text{softmax}(z)_i = \exp(z_i) / \sum_j \exp(z_j)$. Generalizes sigmoid to multinomial distributions. Used for classification output.
  
- **Radial Basis Function (RBF):** $h_i = \exp(-\frac{1}{\sigma_i^2}\|W_{:,i} - x\|^2)$. Saturates to zero for most values; difficult to optimize.

**Cost Functions:**
- Maximum likelihood / negative log-likelihood: $J(\theta) = -E_{x,y \sim \hat{p}_{data}} \log p_{model}(y|x)$. Most common. Equivalent to cross-entropy between data and model distributions.
- Mean squared error (MSE): corresponds to MLE assuming Gaussian output. $J(\theta) = E[\|y - f(x;\theta)\|^2]$. Can saturate with sigmoid/tanh output units; cross-entropy preferred.
- Mean absolute error: corresponds to median prediction. Leads to poor gradient near 0.

**Output Unit Types:**
- **Linear units:** $\hat{y} = W^\top h + b$. For Gaussian output distributions. No saturation. For regression.
- **Sigmoid units:** $\hat{y} = \sigma(w^\top h + b)$. For Bernoulli distributions. Log-likelihood cost avoids saturation problem: $J = -\log\sigma((2y-1)z) = \zeta((1-2y)z)$.
- **Softmax units:** For multinoulli distributions. $z_i = \log\tilde{P}(y=i|x)$. Combined with negative log-likelihood: $J = -z_i + \log\sum_j \exp(z_j)$. Numerically stable version subtracts max.
- **Gaussian mixture outputs:** For multimodal continuous distributions.

**Back-Propagation Algorithm:** Method to compute gradients efficiently through the chain rule. Runs in two passes:
1. **Forward pass:** Compute and store activations at each layer
2. **Backward pass:** Compute gradients from output back to inputs, using chain rule: $\frac{\partial J}{\partial x} = \frac{\partial J}{\partial y} \frac{\partial y}{\partial x}$

Time complexity: $O(n)$ where $n$ is number of edges in computational graph. Memory: $O(\text{depth})$ for activations stored during forward pass.

**Chain Rule (vector case):** $\nabla_x z = \left(\frac{\partial y}{\partial x}\right)^\top \nabla_y z$ where $\frac{\partial y}{\partial x}$ is the Jacobian matrix.

**General Back-Propagation:** Operates on computational graph nodes. For each node $u^{(i)}$ computing $u^{(i)} = f^{(i)}(A^{(i)})$:
$$\frac{\partial u^{(n)}}{\partial u^{(j)}} = \sum_{i: j \in \text{Pa}(u^{(i)})} \frac{\partial u^{(n)}}{\partial u^{(i)}} \frac{\partial u^{(i)}}{\partial u^{(j)}}$$

**Computational Graph:** Formal structure describing computations. Nodes are variables (scalars, vectors, matrices, tensors). Edges represent operations. Back-propagation traverses in reverse. Each edge computes one Jacobian product.

**Symbol-to-Symbol Differentiation (Theano, TensorFlow approach):** Adds derivative nodes to computational graph, enabling higher-order derivatives and lazy evaluation.

**Architecture Design Choices:**
- Number of layers (depth)
- Width of each layer
- Connectivity pattern (skip connections, etc.)
- Universal approximation theorem: A feedforward network with a single hidden layer of sufficient width can approximate any Borel measurable function to any accuracy (Hornik et al., 1989; Cybenko, 1989). But "sufficient width" may be exponential in depth — deep networks are more efficient.

**Universal Approximation:** Deep networks with $O(1)$ width but $O(n)$ depth can approximate functions that require $O(2^n)$ width with shallow networks for some function classes.

**XOR Example:** Linear model cannot learn XOR. Two-layer network with ReLU can: $f(x; W, c, w, b) = w^\top \max\{0, W^\top x + c\} + b$. Specific solution: $W = \begin{pmatrix}1&1\\1&1\end{pmatrix}$, $c = \begin{pmatrix}0\\-1\end{pmatrix}$, $w = \begin{pmatrix}1\\-2\end{pmatrix}$, $b=0$.

**Historical Notes on Back-Propagation:** Independently discovered multiple times. Key developments: Werbos (1981), Parker (1985), Rumelhart et al. (1986). Named "back-propagation" to mean propagating the training signal backward (not reverse-mode automatic differentiation).

### Key Results & Benchmarks
- Universal approximation theorem (Hornik, 1989): Single hidden layer feedforward network is a universal approximator
- Depth efficiency: functions representable by $O(\text{poly}(n))$ parameters with depth $k$ require $O(2^n)$ parameters with depth $k-1$ (Montufar et al., 2014)

### Logical Structure
Chapter 6 is the central technical chapter of Part II. It introduces the core MLP architecture, all major output unit types, cost functions, and back-propagation. Chapters 7-10 add regularization, optimization improvements, and specialized architectures (CNNs, RNNs) to this foundation.

### Notable Quotes
> "The most essential design element of modern neural networks...is the choice of a nonlinear activation function." — p.191

### Cross-Chapter Connections
Back-propagation (section 6.5) is applied to regularized objectives in Chapter 7, optimized using advanced algorithms in Chapter 8, applied to convolutional networks in Chapter 9 and RNNs in Chapter 10. The output unit types here are reused throughout Parts II and III.

---

## Chapter 7: Regularization for Deep Learning

### Core Argument
Regularization — any modification to reduce generalization error without reducing training error — is achieved through many strategies including norm penalties, dropout, and data augmentation; deep learning benefits from multiple complementary regularization approaches because the true data-generating process lies outside any fixed model family.

### Key Concepts & Algorithms

**Regularization Definition:** $\tilde{J}(\theta; X, y) = J(\theta; X, y) + \alpha\Omega(\theta)$, where $\Omega(\theta)$ is a penalty on parameter values and $\alpha \in [0,\infty)$ controls regularization strength.

**L2 Regularization (Weight Decay / Ridge / Tikhonov):** $\Omega(\theta) = \frac{1}{2}\|w\|_2^2$. Gradient update becomes $w \leftarrow (1-\epsilon\alpha)w - \epsilon\nabla_w J$. Effect: rescales weights along Hessian eigenvectors. Dimensions with eigenvalue $\lambda_i \gg \alpha$ are preserved; those with $\lambda_i \ll \alpha$ shrink to near zero. Only directions contributing significantly to reducing objective are preserved. Equivalent to Gaussian prior $p(w) \propto \exp(-\frac{\alpha}{2}w^\top w)$ in MAP estimation.

**L1 Regularization (Lasso):** $\Omega(\theta) = \|w\|_1 = \sum_i |w_i|$. Gradient: $\nabla_w\tilde{J} = \alpha \text{sign}(w) + \nabla_w J$. Produces sparse solutions: $w_i = \text{sign}(w_i^*)\max(|w_i^*| - \alpha/H_{i,i}, 0)$. Equivalent to Laplace prior on weights.

**Norm Penalties as Constrained Optimization:** $\arg\min_\theta J(\theta)$ subject to $\Omega(\theta) \leq k$. Lagrangian approach connects to explicit norm penalties. KKT conditions at optimum require gradient of objective to be proportional to gradient of constraint.

**Dataset Augmentation:** Creating new training examples by applying transformations that preserve class labels. For images: translations, rotations, flips, color jitter, elastic distortions. Most effective for object recognition. Adding noise to inputs is a form of augmentation.

**Noise Robustness:** Injecting noise into inputs, weights, or output labels acts as regularization. Noise on inputs equivalent to L2 penalty under some conditions. Label smoothing: instead of hard targets {0,1}, use $\{\epsilon/(k-1), 1-\epsilon\}$. Prevents overconfidence.

**Semi-Supervised Learning:** Using unlabeled data to help supervised learning. Jointly learn generative model $P(x)$ and discriminative model $P(y|x)$. Representations from generative model can improve discriminative performance.

**Multi-Task Learning:** Sharing parameters between models for different tasks. The part of the model shared across tasks must learn features that are generally useful. Pooling data effectively increases training set size for shared parameters.

**Early Stopping:** Halt training when validation set error begins to increase. Approximately equivalent to L2 regularization: $\epsilon \approx 1/(\alpha\tau)$ where $\tau$ is number of steps and $\alpha$ is weight decay coefficient. Does not require choosing regularization hyperparameter (just early stopping criterion). Most commonly used regularization in practice.

**Parameter Tying and Sharing:** Constraint that parameters in different parts of model must be equal. CNNs are extreme example: weights shared across all spatial positions. Dramatically reduces number of parameters. Can be enforced via soft penalty $\Omega(w^A, w^B) = \|w^A - w^B\|_2^2$.

**Sparse Representations:** Regularizers that encourage representations (not just parameters) to be zero. L1 on hidden units. $k$-sparse activation: only top-$k$ activations allowed.

**Bagging (Bootstrap Aggregating) and Ensemble Methods:** Train multiple different models and average their predictions. Different models make different errors; averaging reduces variance. Deep neural networks can be approximately ensembled cheaply by averaging predictions of subnetworks.

**Dropout (Srivastava et al., 2014):** Training technique that randomly drops (sets to zero) each unit with probability $p$ (typically 0.5 for hidden units, 0.8 for input units) during each training step. At test time, weights multiplied by $1-p$ (weight scaling). Trains exponentially many models sharing parameters. Key effects:
- Forces each unit to be independently useful
- Prevents co-adaptation of feature detectors
- Acts as form of bagging with shared parameters
- Effect similar to L2 weight decay but more multiplicative
Inference: approximate ensemble prediction using weight scaling. Monte Carlo inference: sample many masks and average predictions. Dropout is much stronger regularizer than weight decay for deep networks.

**Adversarial Training:** Training on adversarial examples — inputs specifically designed to cause misclassification. Linear models vulnerable to $\text{sign}(\nabla_x J(\theta, x, y))$ perturbations. Training on these inputs reduces model's vulnerability. Also reveals model's ability to generalize between multiple inputs mapped to same representation.

**Tangent Distance, Tangent Propagation, Manifold Tangent Classifier:** Regularization methods exploiting manifold structure. Tangent distance: classifies using distance along manifold surface, not in ambient space. Tangent propagation: adds regularization penalty $\Omega = \sum_i (J f - J_t)^2$ penalizing sensitivity to known transformations.

**Batch Normalization (Ioffe and Szegedy, 2015):** (mentioned in context of regularization) Normalizes activations within a minibatch: $\hat{x}^{(k)} = (x^{(k)} - \mu_B) / \sqrt{\sigma_B^2 + \epsilon}$. Then applies learned scale $\gamma$ and shift $\beta$: $y^{(k)} = \gamma^{(k)}\hat{x}^{(k)} + \beta^{(k)}$. Reduces internal covariate shift. Acts as regularizer (reduces need for dropout). Allows higher learning rates.

### Key Results & Benchmarks
- Dropout reduced error on MNIST, CIFAR, ImageNet benchmarks by large margins vs. no regularization (Srivastava et al., 2014)
- On some benchmarks, Dropout provides similar regularization to ensembling thousands of networks
- L2 regularization analysis shows weights preserved along Hessian eigenvectors with large eigenvalues, shrunk along directions with small eigenvalues

### Logical Structure
Chapter 7 catalogs all major regularization strategies. Early stopping and dropout are the most important in practice. The chapter connects regularization to Bayesian inference (MAP estimation) and to ensemble methods, showing that regularization is not just a practical trick but has principled foundations.

### Cross-Chapter Connections
Regularization connects to optimization (Ch 8 early stopping) and initialization (Ch 8 weight scale). Dropout is critical for Chapters 9-10 (CNNs, RNNs). Chapter 15 (representation learning) addresses how pretraining regularizes.

---

## Chapter 8: Optimization for Training Deep Models

### Core Argument
Training deep networks involves optimization in a non-convex, high-dimensional space with unique challenges (saddle points, exploding/vanishing gradients, ill-conditioning) that require specialized algorithms beyond standard optimization; stochastic gradient descent and its adaptive variants are the dominant approaches, enhanced by momentum and careful initialization.

### Key Concepts & Algorithms

**Empirical Risk Minimization (ERM):** Replace true distribution with empirical: $\frac{1}{m}\sum_i L(f(x^{(i)};\theta), y^{(i)})$. Machine learning optimizes a proxy for the true objective.

**Surrogate Loss Functions:** Cross-entropy loss used as surrogate for 0-1 loss. Can continue decreasing even after 0-1 loss reaches zero. Can learn more robust features.

**Minibatch Stochastic Gradient Descent:** Standard error of gradient estimate: $\sigma/\sqrt{m}$. Less than linear returns from larger batches. Typical batch sizes: 32-256 (powers of 2 for GPU efficiency). Small batches add noise that acts as regularization.

**Challenges in Neural Network Optimization:**

1. **Ill-Conditioning:** Hessian with large condition number means gradient descent takes very small steps due to curvature. Test: monitor $g^\top H g / g^\top g$. If ratio grows, ill-conditioning is the issue.

2. **Local Minima:** Modern understanding: most local minima in large networks are near global minimum. Model non-identifiability (weight space symmetry, sign flips for ReLU) creates many equivalent local minima, all with same cost. True problematic local minima are rare for sufficiently large networks. (Saxe et al., 2013; Dauphin et al., 2014; Goodfellow et al., 2015)

3. **Saddle Points:** More common than local minima in high dimensions. For functions with many dimensions where eigenvalue signs are random, probability of all positive (local min) is $2^{-n}$. Gradient can vanish near saddle points. SGD can escape saddle points empirically. Newton's method attracted to saddle points — major problem.

4. **Cliffs and Exploding Gradients:** Extremely steep regions from multiplying many large weights. Solution: gradient clipping — rescale gradient when its norm exceeds threshold $v$: $g \leftarrow g \cdot v / \|g\|$ when $\|g\| > v$.

5. **Vanishing and Exploding Gradients:** When same weight matrix $W$ applied $t$ times: $W^t = V\text{diag}(\lambda)^t V^{-1}$. Eigenvalues $|\lambda_i| > 1$ explode, $|\lambda_i| < 1$ vanish. Critical for RNNs. Vanishing makes it hard to learn long-term dependencies. Exploding makes learning unstable.

6. **Inexact Gradients:** Minibatch estimates introduce noise. Some objectives (e.g., Boltzmann machine log-likelihood) have intractable exact gradients requiring approximation.

7. **Poor Correspondence between Local and Global Structure:** Local gradient may not point toward distant regions of lower cost. SGD trajectories spend much time traversing flat regions or going around mountains.

**Stochastic Gradient Descent (SGD):**
$$\theta \leftarrow \theta - \epsilon \hat{g}$$
where $\hat{g} = \frac{1}{m}\nabla_\theta \sum_i L(f(x^{(i)};\theta), y^{(i)})$
Convergence: $\sum_k \epsilon_k = \infty$ and $\sum_k \epsilon_k^2 < \infty$. Linear decay schedule to $\epsilon_\tau$ by iteration $\tau$.

**Momentum:** Accumulates exponentially decaying moving average of gradient, continues moving in that direction.
$$v \leftarrow \alpha v - \epsilon \nabla_\theta \frac{1}{m}\sum_i L(f(x^{(i)};\theta), y^{(i)})$$
$$\theta \leftarrow \theta + v$$
Terminal velocity: $\|g\|/(1-\alpha)$. Common $\alpha$ values: 0.5, 0.9, 0.99. Addresses both poor Hessian conditioning and noisy gradients.

**Nesterov Momentum (Sutskever et al., 2013):** Evaluates gradient at anticipated future position: $\nabla_\theta J(\theta + \alpha v)$. In convex batch case, improves convergence from $O(1/k)$ to $O(1/k^2)$. No improvement for SGD.

**AdaGrad (Duchi et al., 2011):** Adapts learning rates per parameter by scaling inversely to sum of squared historical gradients. $r \leftarrow r + g \odot g$, $\theta \leftarrow \theta - \frac{\epsilon}{\delta + \sqrt{r}} \odot g$. Performs well for sparse gradients. Can cause premature stopping for deep networks due to accumulating history.

**RMSProp (Hinton, 2012):** Modifies AdaGrad with exponentially decaying moving average of squared gradients: $r \leftarrow \rho r + (1-\rho) g \odot g$. Discards distant history. One of the most widely used optimizers for deep networks.

**Adam (Kingma and Ba, 2014):** Combines momentum with RMSProp. First moment: $s \leftarrow \rho_1 s + (1-\rho_1)g$. Second moment: $r \leftarrow \rho_2 r + (1-\rho_2)g\odot g$. Bias correction: $\hat{s} = s/(1-\rho_1^t)$, $\hat{r} = r/(1-\rho_2^t)$. Update: $\theta \leftarrow \theta - \epsilon \hat{s}/\sqrt{\hat{r}} + \delta$. Suggested defaults: $\epsilon=0.001$, $\rho_1=0.9$, $\rho_2=0.999$, $\delta=10^{-8}$. Generally robust to hyperparameter choice.

**Newton's Method:** $\theta^* = \theta - H^{-1}\nabla_\theta J(\theta)$. Scales $O(k^2)$ in memory and $O(k^3)$ in computation for $k$ parameters. Attracted to saddle points. Not practical for modern networks.

**Conjugate Gradients:** Finds conjugate directions that don't undo previous optimization steps. Nonlinear conjugate gradients extend to non-quadratic objectives. Rarely used in deep learning.

**Natural Gradient:** Follows steepest descent in the space of distributions rather than parameters. Fisher information matrix preconditioning. Connections to Newton's method. Approximated by K-FAC (Martens and Grosse, 2015).

**Parameter Initialization:**
- Must break symmetry: different initial parameters for different units
- Weights typically drawn from Gaussian or uniform distribution
- Xavier/Glorot initialization: $W_{i,j} \sim U\left(-\sqrt{\frac{6}{m+n}}, \sqrt{\frac{6}{m+n}}\right)$ where $m$ inputs, $n$ outputs. Balances variance of activations and gradients.
- Biases: typically 0, or 0.1 for ReLU (prevents dead units)
- LSTM forget gate bias: recommend initializing to 1 (Jozefowicz et al., 2015)
- Orthogonal initialization (Saxe et al., 2013): random orthogonal weight matrix with appropriate gain factor $g$ based on nonlinearity
- Sparse initialization (Martens, 2010): each unit has exactly $k$ non-zero connections

**Batch Normalization (Ioffe and Szegedy, 2015):** Normalizes activations within minibatch then applies learned affine transform. During training: $\hat{x} = (x - \mu_B)/\sqrt{\sigma_B^2 + \epsilon}$, $y = \gamma\hat{x} + \beta$. During inference: use running average statistics. Reduces covariate shift, allows higher learning rates, acts as regularizer. Can be applied before or after activation function.

**Optimization Strategies:**
- **Curriculum Learning (Bengio et al., 2009):** Train on easier examples first, gradually increase difficulty. Analogous to human education.
- **Polyak Averaging:** Parameter estimates are average of iterates $\hat{\theta}^{(t)} = \frac{1}{t}\sum_i \theta^{(i)}$. Can reduce variance.
- **Greedy supervised pretraining:** Train each layer separately, then fine-tune jointly.

### Key Results & Benchmarks
- Local minima: for large networks, most local minima have low cost comparable to global minimum (Saxe et al., 2013; Choromanska et al., 2014)
- Saddle points: proliferate in high dimensions; SGD generally escapes them (Goodfellow et al., 2015 visualizations)
- Adam: robust to hyperparameter choice; one of the most widely used optimizers
- Gradient clipping: essential for stable RNN training

### Logical Structure
Chapter 8 catalogs the full optimization toolkit. SGD and its adaptive variants form the foundation. The analysis of why pure optimization fails (non-convexity, saddle points) motivates the heuristic but effective approaches used in practice.

### Cross-Chapter Connections
Optimization applies throughout Part II. RNN-specific optimization challenges (exploding/vanishing gradients) are further addressed in Chapter 10. Chapter 12 discusses large-scale distributed optimization.

---

## Chapter 9: Convolutional Networks

### Core Argument
Convolutional neural networks (CNNs) achieve efficient learning for grid-structured data (images, audio, sequences) by exploiting three key properties: sparse interactions, parameter sharing (weight tying), and equivariant representations.

### Key Concepts & Algorithms

**Convolution Operation:** $s(t) = (x * w)(t) = \int x(a)w(t-a)da$ (continuous). Discrete: $s(t) = \sum_a x(a)w(t-a)$. In ML: input (feature map), kernel (filter), output (feature map). 2D: $S(i,j) = (I * K)(i,j) = \sum_m\sum_n I(i-m, j-n)K(m,n)$.

**Cross-Correlation (used in practice, often called "convolution"):** $S(i,j) = \sum_m\sum_n I(i+m, j+n)K(m,n)$. No kernel flipping. Learning algorithm learns correct kernel either way.

**Three Key Motivations for Convolution:**
1. **Sparse Interactions:** Kernel size $k \ll m$ input size. Only $k \times n$ parameters vs. $m \times n$ for dense layers. $O(k \times n)$ runtime vs. $O(m \times n)$.
2. **Parameter Sharing:** Same kernel applied at every spatial position. Instead of learning separate parameters per location, a single kernel is learned. Dramatically reduces memory and computation.
3. **Equivariant Representations:** $f(g(x)) = g(f(x))$ where $g$ is translation. Translation of input causes corresponding translation of feature map. Suitable for detecting features regardless of position.

**Pooling:** Reduces spatial dimension of feature maps by summarizing local neighborhoods.
- **Max pooling:** Takes maximum of $k \times k$ window. Invariant to small translations. Helps tolerate image distortions.
- **Average pooling:** Takes average. Smooths features.
- **L2 norm pooling:** Takes L2 norm of patch.
- **Strided convolution:** Alternative to pooling that reduces spatial size while learning downsampling.

**Pooling as Infinitely Strong Prior:** Using pooling is like adding prior that learned features are invariant to small translations. This may cause loss of position information, which is sometimes harmful.

**Variants of Convolution:**
- **Strided:** Compute convolution at every $s$ steps. Equivalent to subsampling after full convolution. Used for downsampling.
- **Padded:** Pad input with zeros to control output size. 'Valid' (no padding): output smaller than input. 'Same' (half-padding): output same size as input. 'Full' (padding = kernel_size - 1): every input pixel is visited kernel_size times.
- **Dilated (Atrous):** Insert gaps of size $d-1$ between kernel elements. Increases receptive field without increasing parameters.
- **Transposed Convolution (Fractionally Strided):** Learns upsampling operation. Used in generative models and segmentation.
- **Separable Convolution:** Factorizes $k \times k$ convolution into $k \times 1$ and $1 \times k$ convolutions. Reduces computation from $O(k^2)$ to $O(2k)$ per output pixel.

**Local vs. Global Interactions:** Neurons in deep convolutional layers have large **receptive fields** — the set of input pixels that affect them. Depth enables global interaction through composition of local interactions.

**Structured Outputs:** CNNs can produce spatial maps as output (for segmentation, depth estimation, etc.) rather than class labels.

**CNNs for Different Data Types:**
- 1D: audio, speech, time series. Temporal convolution.
- 2D: images. Standard spatial convolution.
- 3D: video or volumetric medical data. Spatiotemporal convolution.

**Neuroscientific Basis:** Simple and complex cells in primary visual cortex (V1) inspired CNN design. Simple cells: respond to oriented bars at specific locations. Complex cells: respond to oriented bars regardless of position (pooling over simple cell responses). Neocognitron (Fukushima, 1980) first computational model. LeNet (LeCun et al., 1998) the first major practical CNN.

**Historical CNN Achievements:**
- LeNet-5 (LeCun et al., 1998): First successful deep CNN for MNIST digit recognition
- AlexNet (Krizhevsky et al., 2012): Won ImageNet challenge by large margin (26.2% top-5 error vs. 26.2% for second best). First modern deep CNN at scale.
- GoogLeNet/Inception: Used 1×1 convolutions for dimensionality reduction. Reduced parameters.
- VGGNet (Simonyan and Zisserman): Very deep networks (16-19 layers) with 3×3 kernels.

**Efficient Convolution:** Can be implemented as matrix multiplication (im2col method). FFT-based convolution efficient for large kernels: $O(n^2 \log n)$ vs. $O(n^2 k^2)$ for kernel size $k$.

**Random and Unsupervised Features:** Convolutional feature extractors can be learned unsupervised (sparse coding, RBMs) or even randomly initialized and fixed. Fixed random convolutional features can perform reasonably well, showing structure of CNNs contributes to performance independently of learned weights.

### Key Results & Benchmarks
- AlexNet (2012): ~15.3% top-5 error on ImageNet vs. ~26% for previous best non-deep method
- 3×3 kernels (VGGNet): two 3×3 convolutions have same receptive field as one 5×5 but fewer parameters and more nonlinearities
- Pooling invariance: max pooling provides ~20% spatial translation invariance

### Logical Structure
Chapter 9 introduces CNNs as the key architecture for spatial/temporal data. The three motivating properties (sparse interactions, parameter sharing, equivariance) provide principled justification. Historical results contextualize the power of CNNs. Chapter 10 applies similar parameter-sharing ideas to sequences.

### Cross-Chapter Connections
CNN architecture choices informed by Chapter 11 (practical methodology). CNNs applied to computer vision in Chapter 12. Convolutional generative networks appear in Chapter 20 (GANs). Chapter 10 parallels CNN parameter sharing with RNN parameter sharing.

---

## Chapter 10: Sequence Modeling: Recurrent and Recursive Nets

### Core Argument
Recurrent neural networks (RNNs) process sequential data by sharing parameters across time steps via a hidden state, enabling variable-length sequence modeling; however, the vanishing and exploding gradient problems make learning long-term dependencies difficult, motivating gated architectures like LSTM and GRU.

### Key Concepts & Algorithms

**Recurrent Neural Network (RNN):** Neural network specialized for sequential data $x^{(1)}, ..., x^{(\tau)}$. Key equation: $h^{(t)} = f(h^{(t-1)}, x^{(t)}; \theta)$. Same parameters $\theta$ applied at every time step. Hidden state $h^{(t)}$ is a lossy summary of past sequence.

**Computational Graph Unfolding:** Recurrent computation $h^{(t)} = f(h^{(t-1)}, x^{(t)}; \theta)$ can be unfolded into a feedforward graph of depth $\tau$. Advantages: uniform input size regardless of sequence length; single shared transition function $f$.

**Basic RNN Equations (with softmax output):**
$$a^{(t)} = b + Wh^{(t-1)} + Ux^{(t)}$$
$$h^{(t)} = \tanh(a^{(t)})$$
$$o^{(t)} = c + Vh^{(t)}$$
$$\hat{y}^{(t)} = \text{softmax}(o^{(t)})$$
Parameters: $U$ (input-to-hidden), $W$ (hidden-to-hidden), $V$ (hidden-to-output), $b, c$ (biases).

**Total Loss:** $L(\{x^{(1)},...,x^{(\tau)}\}, \{y^{(1)},...,y^{(\tau)}\}) = \sum_t L^{(t)} = -\sum_t \log p_{model}(y^{(t)} | x^{(1)},...,x^{(t)})$

**Back-Propagation Through Time (BPTT):** Applying back-propagation to the unfolded graph. Cost $O(\tau)$ in time and memory. Cannot be parallelized due to sequential dependencies.

**Turing Completeness of RNNs:** A finite-size RNN can simulate any Turing machine computation (Siegelmann and Sontag, 1991). 886 units suffice for universal computation (Siegelmann and Sontag, 1995).

**Teacher Forcing:** During training, use ground truth output $y^{(t)}$ as next input rather than model output $\hat{y}^{(t)}$. Decouples time steps during training, enabling parallelization. Risk: exposure bias — model never sees its own errors during training.

**Bidirectional RNNs (Schuster and Paliwal, 1997):** Combine forward RNN (left-to-right) with backward RNN (right-to-left). Output at each time step incorporates both past and future context. Used in speech recognition, handwriting recognition, NLP.

**Encoder-Decoder / Sequence-to-Sequence Architecture (Cho et al., 2014; Sutskever et al., 2014):** Encoder RNN reads input sequence and produces fixed-length context vector $C$ (typically final hidden state). Decoder RNN generates output sequence conditioned on $C$. Allows variable-length inputs and outputs. Limitation: single fixed-length vector must encode entire input — bottleneck for long sequences.

**Deep Recurrent Networks:** Can have depth in: (1) hidden state stack (multiple hidden layers per time step), (2) input-to-hidden mapping, (3) hidden-to-output mapping. Graves et al. (2013): first to show significant benefit from decomposing state into multiple layers.

**Recursive Neural Networks:** Tree-structured computation graph instead of chain. Can model sentence parse trees, scene graphs. Parameter count does not grow with sequence length.

**The Challenge of Long-Term Dependencies:** Information from time step $t$ affects gradient at time step $t'$: factor of $\prod_{t=t'}^{t-1} \frac{\partial h^{(t+1)}}{\partial h^{(t)}}$. Eigenvalues of this product vanish or explode exponentially with distance. Discovered by Hochreiter (1991), Bengio et al. (1993, 1994). Empirical finding: SGD fails to learn dependencies across >10-20 time steps.

**Paradox of Vanishing Gradients:** Any model capable of robustly storing long-term memories must be in a regime where gradients vanish. The only way to robustly store memories in the presence of perturbations is to use dynamics that are contractive (attractor dynamics), which necessarily cause vanishing gradients (Bengio et al., 1993, 1994).

**Echo State Networks (ESNs):** Fix the recurrent weights such that the hidden state captures past inputs richly; only learn output weights (convex optimization). Set spectral radius of recurrent weight matrix near 1.0. "Reservoir computing" approach.

**Leaky Units:** Hidden units with linear self-connections $h_t^{(i)} \leftarrow \alpha h_{t-1}^{(i)} + (1-\alpha) f(h_{t-1}, x_t; \theta)$ where $\alpha \approx 1$ acts like a running average. Allows gradients to flow for longer time horizons.

**Long Short-Term Memory (LSTM) (Hochreiter and Schmidhuber, 1997):**
Core contribution: self-loops with gated weights, allowing the time scale of integration to be dynamic and data-dependent.

Cell state update:
$$s_i^{(t)} = f_i^{(t)} s_i^{(t-1)} + g_i^{(t)} \sigma\left(b_i + \sum_j U_{i,j} x_j^{(t)} + \sum_j W_{i,j} h_j^{(t-1)}\right)$$

Forget gate: $f_i^{(t)} = \sigma\left(b_i^f + \sum_j U_{i,j}^f x_j^{(t)} + \sum_j W_{i,j}^f h_j^{(t-1)}\right)$ — controls how much of previous cell state to retain.

Input gate: $g_i^{(t)} = \sigma\left(b_i^g + \sum_j U_{i,j}^g x_j^{(t)} + \sum_j W_{i,j}^g h_j^{(t-1)}\right)$ — controls how much new information to add.

Output: $h_i^{(t)} = \tanh(s_i^{(t)}) q_i^{(t)}$

Output gate: $q_i^{(t)} = \sigma\left(b_i^o + \sum_j U_{i,j}^o x_j^{(t)} + \sum_j W_{i,j}^o h_j^{(t-1)}\right)$ — controls what to output.

LSTM initialization: recommend bias of 1.0 for forget gate.

LSTM applications: speech recognition (17.7% phoneme error rate on TIMIT, Graves et al. 2013), machine translation, image captioning.

**Gated Recurrent Unit (GRU) (Cho et al., 2014):** Simpler than LSTM — single gate controls both forgetting and input. Update gate $u$ and reset gate $r$:
$$h_i^{(t)} = u_i^{(t-1)} h_i^{(t-1)} + (1 - u_i^{(t-1)}) \sigma\left(b_i + \sum_j U_{i,j} x_j^{(t)} + \sum_j W_{i,j} r_j^{(t-1)} h_j^{(t-1)}\right)$$
Performance comparable to LSTM. Jozefowicz et al. (2015): comparing architectures, LSTM typically best but GRU competitive.

**Gradient Clipping:** Rescale gradient when norm exceeds threshold: if $\|g\| > v$, then $g \leftarrow g \cdot v/\|g\|$. Essential for stable RNN training (Pascanu et al., 2013).

**Neural Turing Machines (NTM) / Memory-Augmented Networks:** RNNs augmented with external memory. Can read and write to memory using soft attention. Allows learning to sort, recall patterns, etc.

### Key Results & Benchmarks
- LSTM phoneme error rate on TIMIT: 17.7% (Graves et al., 2013, deep bidirectional LSTM), compared to 26% for traditional HMM-GMM
- Sequence-to-sequence (Sutskever et al., 2014): state-of-the-art machine translation using LSTM
- Bengio et al. (1994): probability of successful training via SGD rapidly approaches 0 for sequence lengths 10-20 without gating

### Logical Structure
Chapter 10 extends the computational graph unfolding idea to sequences. The LSTM solves the core challenge identified (vanishing/exploding gradients) through gating. The encoder-decoder framework enables variable-length sequence transformations critical for NLP.

### Cross-Chapter Connections
Chapter 12 applies RNNs to speech recognition and NLP, including attention mechanisms (extending encoder-decoder). Chapter 20 applies RNNs in generative models. Attention mechanism from section 10.4 is foundational to transformer architectures (not yet in this book, published 2016).

---

## Chapter 11: Practical Methodology

### Core Argument
Effective deep learning requires a systematic approach to model selection, hyperparameter tuning, and debugging, guided by specific performance metrics appropriate to the application.

### Key Concepts & Algorithms

**Performance Metrics:**
- Accuracy vs. precision/recall tradeoff in class-imbalanced problems
- Coverage: fraction of examples the model can make a decision on (with rejection option)
- Mean Average Precision for detection tasks
- ROC curves and AUC for threshold-independent evaluation
- Business/deployment metrics may differ from research metrics

**Default Baseline:**
1. Decide what to fix first (data, model, features)
2. Use established baseline model (logistic regression, MLP, CNN, RNN depending on data type)
3. Use ReLU activations, Adam optimizer, batch normalization
4. Track training/validation errors to diagnose underfitting vs. overfitting

**Diagnosing Underfitting vs. Overfitting:**
- If training error too high: model capacity too low or optimization issues → larger model, better optimizer
- If validation error much higher than training error: overfitting → regularization, more data, smaller model
- If gap is acceptable but validation error still too high: may need more data

**Determining Whether to Gather More Data:**
- Plot learning curve: training/validation error vs. training set size
- If validation error decreases with more data → collect more
- If training and validation error have converged → algorithmic changes needed

**Selecting Hyperparameters:**
- Manual search: use expert knowledge to narrow search space
- Grid search: exhaustive search over combinations of discrete values
- Random search (Bergstra and Bengio, 2012): outperforms grid search in most cases. Random search more efficient because models are often insensitive to some hyperparameters.
- Bayesian hyperparameter optimization: model hyperparameter search itself as Bayesian inference
- Important hyperparameters: learning rate (most important), batch size, number of layers, units per layer, weight decay, dropout rate

**Learning Rate Sensitivity:**
- Too high: divergence or oscillation
- Too low: slow convergence or local optimum
- One suggested heuristic: scan learning rates from $10^{-5}$ to 1, observe which range gives decreasing loss

**Debugging Strategies:**
1. **Visualize model in action:** Look at specific incorrect predictions — reveals data issues, distribution shift
2. **Visualize worst cases:** Identify systematic error patterns
3. **Fit a tiny dataset:** Can gradient descent correctly fit 1-10 examples? Validates model implementation
4. **Back-propagation implementation check:** Compare numerical and analytical gradients: $\frac{f(x+\epsilon) - f(x-\epsilon)}{2\epsilon} \approx \frac{df}{dx}$ at $x$
5. **Monitor activations and gradients:** Are they in reasonable ranges? (not zero, not explosive)
6. **Baseline comparison:** Compare against the simplest possible baseline

**Multi-Digit Number Recognition Example:** Shows full pipeline from problem definition to deployed system, illustrating the entire methodology.

### Logical Structure
Chapter 11 bridges theoretical knowledge and practical application. It provides decision trees for common failure modes and establishes the debugging mindset essential for real ML projects.

### Cross-Chapter Connections
Draws on regularization (Ch 7), optimization (Ch 8), and specific architectures (Ch 9-10). Provides practical guidance for applying everything in Part II.

---

## Chapter 12: Applications

### Core Argument
Deep learning has achieved transformative results in computer vision, speech recognition, NLP, and other domains through architecture specializations appropriate to each domain's structure.

### Key Concepts & Algorithms

**Large-Scale Deep Learning Infrastructure:**
- GPU computing: parallel matrix operations, high memory bandwidth. 3-10x speedup over CPU for neural networks. Raina et al. (2009) first to use GPUs for deep learning at scale.
- Data parallelism: replicate model across multiple GPUs/machines, each processes different minibatch
- Model parallelism: split model across devices
- Asynchronous SGD (Recht et al., 2011; Dean et al., 2012): multiple workers update parameters asynchronously without locking. Parameter server stores shared parameters.
- Model compression (Bucilua et al., 2006): train smaller model to mimic larger model's outputs. Applies when large model needed to avoid overfitting but small model needed for inference.

**Computer Vision:**
- Preprocessing: pixel normalization to [0,1] or [-1,1]; global contrast normalization (GCN) standardizes image standard deviation; local contrast normalization (LCN) normalizes within local windows
- Dataset augmentation: random crops, flips, rotations, color jitter. AlexNet preprocessing: only subtract mean pixel.
- Object recognition: AlexNet (2012) breakthrough. Deep CNNs now achieve near-human performance on many benchmarks.
- Object detection: region proposals + CNN classification
- Segmentation: pixel-wise labeling using fully convolutional networks
- Face recognition, medical imaging, autonomous driving

**Speech Recognition:**
- Historical: GMM-HMM dominated 1980s-2009. First wave used neural nets to improve GMM-HMM systems.
- 2009-2012 breakthrough: deep networks with RBM pretraining. Phoneme error on TIMIT: 26% → 20.7% (Mohamed et al., 2009, 2012)
- Later: shift to ReLU, dropout (no pretraining needed). Hinton et al. (2012): 30% WER reduction — unprecedented improvement
- End-to-end: deep LSTM (Graves et al., 2013): 17.7% phoneme error on TIMIT. Connectionist Temporal Classification (CTC) loss: allows training without explicit alignment between input and output sequences
- 2D convolutional models: treat spectrogram as image (time × frequency)

**Natural Language Processing:**
- n-gram models: $P(x_1,...,x_\tau) = P(x_1,...,x_{n-1})\prod_{t=n}^\tau P(x_t|x_{t-n+1},...,x_{t-1})$. High capacity but no generalization to unseen sequences.
- Neural language models (Bengio et al., 2001, 2003): learn distributed word representations. Word embeddings reduce dimensionality; similar words have similar embeddings.
- Word embeddings/Word2Vec (Mikolov et al., 2013): learn embeddings that capture semantic relationships. Skip-gram model predicts context from word.
- Hierarchical softmax: reduce vocabulary prediction from $O(|V|)$ to $O(\log|V|)$ using binary tree over words.
- Importance sampling: approximate softmax gradient using small subset of vocabulary.
- Noise-contrastive estimation (NCE): train model to distinguish real words from noise samples.
- Machine translation: encoder-decoder with attention (Bahdanau et al., 2015). Attention weights: $c^{(t)} = \sum_i \alpha^{(t,i)} h^{(i)}$ where $\alpha^{(t,i)} = \text{softmax}(\text{relevance}(t, i))$.

**Attention Mechanism (Bahdanau et al., 2015):** Creates variable-length context from sequence instead of fixed-size vector. Weighted average of encoder hidden states: $c^{(t)} = \sum_i \alpha^{(t,i)} h^{(i)}$. Weights $\alpha^{(t,i)}$ from softmax over relevance scores. Differentiable approximation to hard attention/indexing.

### Key Results & Benchmarks
- AlexNet: first deep CNN to win ImageNet (~15.3% top-5 error vs. 26% for runner-up)
- Speech recognition: 30% WER reduction in 2012 (Hinton et al.) — largest improvement in 20 years
- LSTM speech recognition (Graves et al., 2013): 17.7% phoneme error on TIMIT
- Machine translation with attention: matched and exceeded phrase-based SMT

### Logical Structure
Chapter 12 demonstrates that the architectures of Chapters 6-10 solve real problems at scale. The chapter shows domain-specific adaptations while confirming that the core deep learning ideas transfer across domains.

### Cross-Chapter Connections
Applies Chapters 6-10 to real domains. Attention mechanism (section 12.4.5.1) anticipates transformers. Encoder-decoder extends Chapter 10's sequence-to-sequence architecture.

---

## Chapter 13: Linear Factor Models

### Core Argument
Linear factor models — including PCA, ICA, sparse coding, and slow feature analysis — provide interpretable probabilistic latent variable models where observable data is generated by a linear transformation of latent factors, forming building blocks for more complex deep generative models.

### Key Concepts & Algorithms

**Linear Factor Model:** $x = Wh + b + \text{noise}$, where $h$ is a vector of latent variables sampled from a factorial prior $p(h) = \prod_i p(h_i)$.

**Probabilistic PCA:** Special case with isotropic noise $\sigma^2 I$. As $\sigma \to 0$, PCA is recovered. EM algorithm for parameter estimation. Joint distribution: $x \sim \mathcal{N}(b, WW^\top + \sigma^2 I)$.

**Factor Analysis:** Like probabilistic PCA but with diagonal (not isotropic) noise $\Psi = \text{diag}(\sigma^2)$. Latent variables capture dependencies between observed variables.

**Independent Component Analysis (ICA):** Finds sources $h$ that are statistically independent. Requires non-Gaussian priors on $h$ (e.g., Laplace, Student-t). Typical choice: $p(h_i) \propto \exp(-|h_i|)$ (Laplace). Used to separate mixed audio signals (cocktail party problem). Cannot use Gaussian priors — indistinguishable from rotation.

**Sparse Coding (Olshausen and Field, 1996):** Finds sparse representations. Prior: $p(h_i) \propto \exp(-\lambda|h_i|)$ (sparse activations near zero). Training alternates between: (1) infer $h^* = \arg\max_h p(h|x)$ via optimization, (2) update $W$ to improve reconstruction. Dictionary $W$ learned to capture common patterns in data; each example explained by sparse combination of dictionary elements.

**Slow Feature Analysis (SFA) (Wiskott and Sejnowski, 2002):** Finds slowly-varying features in time sequences. Objective: $\min E_t[(f(x^{(t+1)})_i - f(x^{(t)})_i)^2]$ subject to zero mean, unit variance, and orthogonality. Trained on video of natural scenes: learns features resembling V1 complex cells. State-of-art does not use SFA as of 2016.

**Manifold Interpretation of PCA:** Each principal component defines a direction in the data manifold. PCA can be seen as finding the linear manifold closest to the data. Generalized to nonlinear autoencoders in Chapter 14.

### Logical Structure
Chapter 13 introduces probabilistic latent variable models as a simpler precursor to deep generative models. The key ideas (latent factors, sparse representations, statistical independence) recur throughout Part III.

### Cross-Chapter Connections
Linear factor models are building blocks for Chapter 14 (autoencoders), Chapter 15 (representation learning), and Chapter 20 (deep generative models). Sparse coding is used in Chapter 19 (approximate inference via MAP).

---

## Chapter 14: Autoencoders

### Core Argument
Autoencoders learn to compress data into a lower-dimensional representation and reconstruct it, with regularization preventing them from simply learning the identity function; they capture the structure of the data distribution and can be used for representation learning, generative modeling, and manifold learning.

### Key Concepts & Algorithms

**Autoencoder:** Combines encoder $f$ (input → code $h$) and decoder $g$ (code → reconstruction). Trained to minimize $L(x, g(f(x)))$. If unconstrained, learns identity function trivially.

**Undercomplete Autoencoder:** Code dimension less than input dimension. Forces compression, learns most salient features. If linear encoder/decoder with MSE loss, learns PCA subspace. With nonlinear encoder/decoder, learns nonlinear generalization of PCA.

**Overcomplete Autoencoder:** Code dimension greater than or equal to input dimension. Risk of learning identity. Requires additional regularization.

**Regularized Autoencoders:**
- **Sparse Autoencoder:** Adds sparsity penalty $\Omega(h)$ to loss. Penalizes activations. Equivalent to MAP inference with sparse prior on code.
- **Denoising Autoencoder (Vincent et al., 2008):** Train to reconstruct $x$ from corrupted $\tilde{x} = C(\tilde{x}|x)$ (e.g., Gaussian noise, zero masking). Forces model to learn robust features. Equivalent to minimizing reconstruction error under noise distribution: $-\log p_{decoder}(x | h = f(\tilde{x}))$.
  
  Score-based interpretation: denoising autoencoder learns to estimate the score $\nabla_x \log p(x)$ (direction of increasing data density). Sampling from this learned score function yields samples from the data distribution.
  
- **Contractive Autoencoder (CAE) (Rifai et al., 2011):** Adds penalty on Frobenius norm of Jacobian of encoder: $\Omega(h, x) = \lambda \|J_f(x)\|_F^2$. Encourages encoder to be insensitive to small input changes. Learns features tangent to data manifold.

**Representational Power:** Single hidden layer autoencoder can approximate any function. Depth allows efficient representation of complex structure.

**Stochastic Encoders and Decoders:** Stochastic encoder $q_\phi(h|x)$, stochastic decoder $p_\theta(x|h)$. Training maximizes $E_{h\sim q_\phi(h|x)}[\log p_\theta(x|h)]$. Foundation for VAEs.

**Learning Manifolds:** Autoencoders learn the manifold by learning the encoder (mapping onto manifold), decoder (mapping back), and tangent space (local directions of variation). Manifold dimension = code dimension.

**Generative Autoencoders:** Can sample from data distribution by: (1) sampling from learned distribution over codes, (2) decoding sampled codes. Requires model of $p(h)$ — e.g., fitted Gaussian, or using denoising autoencoder's Markov chain.

**Predictive Sparse Decomposition (PSD):** Hybrid of sparse coding and parametric encoder. Jointly trains encoder to predict sparse code and decoder to reconstruct from sparse code.

**Applications:**
- Feature extraction / unsupervised pretraining
- Dimensionality reduction (visualization)
- Anomaly detection: reconstruction error signals anomalies
- Generative modeling (with appropriate constraints on code space)
- Image compression (with deep networks)

### Logical Structure
Chapter 14 establishes autoencoders as a family of unsupervised representation learning methods. The denoising autoencoder connects to score matching and provides foundation for generative models. Chapter 20 develops VAEs as the most powerful autoencoder-based generative model.

### Cross-Chapter Connections
Autoencoders use architectures from Chapter 6. Sparse autoencoders connect to sparse coding (Chapter 13). Denoising autoencoders connect to score matching (Chapter 18). VAEs in Chapter 20 are the probabilistic generalization of autoencoders.

---

## Chapter 15: Representation Learning

### Core Argument
Good representations disentangle the underlying causal factors of variation in data; deep distributed representations are exponentially more efficient than shallow ones; transfer learning and semi-supervised learning leverage representations learned in one context for another.

### Key Concepts & Algorithms

**What Makes a Good Representation:**
- Makes subsequent learning task easier
- Disentangles factors of variation
- Distributed representations: exponentially more efficient than local (one-hot)
- Smooth, with appropriate invariances

**Greedy Layer-Wise Unsupervised Pretraining:** Train each layer independently with unsupervised objective, then fine-tune the whole network with supervised learning. Key to 2006 deep learning renaissance (Hinton et al., 2006; Bengio et al., 2007). Today mostly abandoned except for NLP (word embeddings).

**When Pretraining Works:**
- More useful with very deep networks
- More useful with small labeled sets, large unlabeled sets
- More useful for NLP (word one-hot vectors contain no similarity information)
- Less useful when supervised data is abundant

**Transfer Learning:** Knowledge from one task/distribution $P_1$ transferred to another $P_2$. Common approach: pretrain on large labeled dataset, fine-tune on small target dataset. ImageNet pretrained CNNs used as feature extractors for many vision tasks (Oquab et al., 2014; Yosinski et al., 2014).

**Domain Adaptation:** Same task, different input distribution. Unsupervised pretraining (denoising autoencoders) very effective for sentiment analysis across domains (Glorot et al., 2011).

**Multi-Task Learning:** Multiple tasks share lower layers, have task-specific upper layers. Shared layers learn generally useful representations. Pooling examples from all tasks increases effective training set size.

**Semi-Supervised Disentangling of Causal Factors:** Hypothesis: good representation captures the true generative factors of the data. Temporal coherence (slowness principle), smoothness, sparsity, and other priors can help discover causal structure.

**Distributed Representation:** Exponential gain: with $k$ features each taking $n$ values, can represent $n^k$ concepts. Compare to one-hot with $n^k$ separate detectors. Deep distributed representations are even more powerful.

**Exponential Gains from Depth (Montufar et al., 2014):** Depth-$k$ ReLU network can represent piecewise-linear functions with exponentially many linear regions: $O(\binom{n}{d}^{k-1} n^d)$ regions for width $n$ and depth $k$. Width-$n$ depth-1 network has $O(2^n)$ regions at most.

**Clues to Discover Underlying Causes:**
- Smoothness / local constancy prior
- Temporal coherence (similar causes persist over time)
- Sparsity (few causes active at once)
- Simplicity of factor dependencies
- Manifold structure

### Key Results & Benchmarks
- Pretraining (Erhan et al., 2010): networks with pretraining consistently terminate in different (smaller) region of function space; reduced variance of estimation
- Transfer learning: pretrained ImageNet features dramatically outperform random initialization on small datasets
- Distributed representation efficiency: $n$ features can represent $2^n$ possible inputs vs. $n$ inputs for local representations

### Logical Structure
Chapter 15 provides the theoretical justification for why deep learning works: depth enables exponentially efficient representations of complex functions, and shared representations enable transfer across tasks. This chapter unifies Part I and Part II concepts under the framework of representation learning.

### Cross-Chapter Connections
Connects to Chapters 13-14 (specific representation learning methods), anticipates Chapter 20 (generative models learn representations). Pretraining (section 15.1) is now largely historical but important for understanding the field's evolution.

---

## Chapter 16: Structured Probabilistic Models for Deep Learning

### Core Argument
Graphical models provide a language for representing independence structure in probability distributions, enabling tractable learning and inference in high-dimensional spaces by decomposing joint distributions into smaller factors.

### Key Concepts & Algorithms

**Challenge of Unstructured Modeling:** Representing a joint distribution over $n$ binary variables requires $2^n - 1$ parameters. Must use structured models that exploit conditional independence.

**Directed Graphical Models (Bayesian Networks):** Represent $p(x) = \prod_i p(x_i | \text{parents}(x_i))$. Arrows indicate direct probabilistic dependence. Ancestral sampling: sample variables in topological order. Explaining away: observing a child can create dependence between parents.

**Undirected Graphical Models (Markov Random Fields):** $p(x) = \frac{1}{Z}\prod_i \phi^{(i)}(\mathcal{C}^{(i)})$ where $\phi$ are non-negative compatibility functions (clique potentials) and $Z = \sum_x \prod_i \phi^{(i)}(\mathcal{C}^{(i)})$ is the partition function (intractable in general). Edges indicate potential interaction.

**Energy-Based Models:** $p(x) = \exp(-E(x))/Z$ where $E$ is an energy function. Lower energy = higher probability. Boltzmann machines are an example.

**Restricted Boltzmann Machines (RBMs):** $E(v,h) = -b^\top v - c^\top h - v^\top Wh$. Bipartite structure (no within-layer connections): $P(h_j=1|v) = \sigma(c_j + W_{:,j}^\top v)$ and $P(v_i=1|h) = \sigma(b_i + W_{i,:}h)$. Conditional distributions are factorial — enables efficient block Gibbs sampling.

**Partition Function:** $Z = \sum_{x} \exp(-E(x))$. Intractable for most models (sum over $2^n$ states). Learning requires approximating $\nabla_\theta \log Z$.

**Latent Variables:** Introduce $h$ not directly observed to capture higher-order interactions. Marginalizing: $p(v) = \sum_h p(v,h)$. Key to expressiveness of Boltzmann machines.

**Inference:** Computing $p(h|v)$ or other conditional distributions given observations. Often intractable; requires approximation.

**Deep Learning Approach:** Use deep neural networks to represent factors. Connect directed and undirected models. Train with approximate inference (variational, MCMC).

### Logical Structure
Chapter 16 provides the probabilistic graphical model vocabulary used in Chapters 17-20. Energy-based models, RBMs, and directed/undirected distinctions are essential for understanding deep generative models.

---

## Chapter 17: Monte Carlo Methods

### Core Argument
Monte Carlo methods estimate expectations via random sampling, enabling tractable approximate inference and learning in probabilistic models where exact computation is intractable.

### Key Concepts & Algorithms

**Monte Carlo Estimation:** $E_p[f(x)] \approx \frac{1}{n}\sum_{i=1}^n f(x^{(i)})$ where $x^{(i)} \sim p$. Variance decreases as $O(1/n)$. Unbiased.

**Importance Sampling:** Sample from proposal $q(x) \neq p(x)$. Correct via weights: $E_p[f(x)] \approx \sum_i w_i f(x^{(i)}) / \sum_i w_i$ where $w_i = p(x^{(i)})/q(x^{(i)})$. Choice of $q$ critically affects variance. Optimal $q^*(x) \propto p(x)|f(x)|$.

**Markov Chain Monte Carlo (MCMC):** When direct sampling from $p$ is intractable, construct Markov chain with $p$ as stationary distribution. Burn-in period required. Key challenge: mixing time (how long to reach stationary distribution).

**Gibbs Sampling:** MCMC method that samples each variable conditioned on all others. For RBMs: alternate between sampling $h$ given $v$ and sampling $v$ given $h$ (block Gibbs sampling). Efficient when conditional distributions are tractable.

**Challenge of Mixing:** When distribution has multiple well-separated modes (peaks), MCMC chains can get stuck in one mode. Difficult to mix between modes. Major challenge for training undirected models like Boltzmann machines.

### Logical Structure
Chapter 17 provides the sampling tools used for training and inference in Chapters 18-20. MCMC is used for approximate inference in RBMs and DBMs. Mixing challenges motivate the contrastive divergence approximation.

---

## Chapter 18: Confronting the Partition Function

### Core Argument
The intractable partition function in undirected probabilistic models makes exact maximum likelihood training impossible; several approximations — contrastive divergence, pseudolikelihood, score matching, noise-contrastive estimation — enable practical training.

### Key Concepts & Algorithms

**Log-Likelihood Gradient Decomposition:** $\frac{\partial \log p(x)}{\partial \theta} = -\frac{\partial E(x)}{\partial\theta} - E_{x \sim p_{model}}\left[\frac{\partial E(x)}{\partial\theta}\right]$. Two phases: positive phase (pushes down energy of data) and negative phase (pushes up energy of model samples). Negative phase requires sampling from model — intractable.

**Contrastive Divergence (CD) (Hinton, 2002):** Approximate negative phase by running MCMC starting from data for $k$ steps. CD-1 (1 step) works surprisingly well in practice. Fast but biased — does not converge to true MLE.

**Stochastic Maximum Likelihood (SML) / Persistent CD (Tieleman, 2008):** Maintain persistent chain of samples (replay buffer). Update chain by a few steps after each parameter update. Better than CD for models that need to mix across modes. Used for training deep Boltzmann machines.

**Pseudolikelihood:** Replace joint likelihood with product of conditional likelihoods: $\prod_i p(x_i | x_{-i})$. Each conditional is tractable. Consistent estimator (converges to correct value with infinite data). Less efficient than MLE but avoids partition function.

**Score Matching (Hyvärinen, 2005):** Minimize $\frac{1}{2}E_p\left[\|\nabla_x \log p_{model}(x;\theta) - \nabla_x \log p_{data}(x)\|^2\right]$. Partition function cancels in gradient. Works for continuous distributions. Computationally expensive for high-dimensional data.

**Noise-Contrastive Estimation (NCE) (Gutmann and Hyvärinen, 2010):** Train classifier to distinguish data from a noise distribution. Treats partition function as a learned parameter. Consistent estimator. Widely used for training neural language models.

**Annealed Importance Sampling (AIS):** Bridge from tractable $p_0$ to target $p_1$ using sequence of intermediate distributions. Provides unbiased estimates of partition function. Used to evaluate generative models.

### Logical Structure
Chapter 18 provides practical methods for training the undirected models introduced in Chapter 16. Contrastive divergence is the key practical algorithm for RBMs.

---

## Chapter 19: Approximate Inference

### Core Argument
When exact probabilistic inference is intractable, variational inference provides a principled framework for approximate inference by optimizing a lower bound on log-likelihood, with the variational autoencoder as the most powerful deep learning application.

### Key Concepts & Algorithms

**Inference as Optimization:** Approximate posterior $q(h|v)$ to minimize $D_{KL}(q(h|v) \| p(h|v))$. Equivalent to maximizing ELBO (Evidence Lower Bound): $\mathcal{L}(v, \theta, q) = \log p(v;\theta) - D_{KL}(q(h|v) \| p(h|v)) \leq \log p(v;\theta)$.

**Expectation Maximization (EM):** Two-step iterative algorithm. E-step: compute $q(h|v) = p(h|v;\theta)$ (true posterior). M-step: update $\theta$ to maximize $E_{h \sim q}[\log p(v, h;\theta)]$. Requires tractable E-step. Generalized EM uses approximate E-step.

**MAP Inference:** Approximate full posterior with point mass at mode: $h^* = \arg\max_h p(h|v)$. For sparse coding: $h^* = \arg\max_h p(h|x) = \arg\max_h [\log p(x|h) + \log p(h)]$. Optimization over $h$ at each training example.

**Variational Inference:** Restrict $q$ to a tractable family (e.g., fully factorized $q(h|v) = \prod_i q(h_i|v)$ — mean-field). Optimize ELBO over the parameters of $q$. Mean field: coordinate ascent over $q(h_i)$ holding others fixed. Used for training DBMs.

**Wake-Sleep Algorithm (Hinton et al., 1995):** Two-phase training. Wake phase: use recognition network to infer $h$ from $v$; update generative parameters. Sleep phase: sample from generative model; update recognition parameters. For training deep belief networks.

**Learned Approximate Inference:** Use neural network (inference network / recognition model) to compute approximate posterior parameters. Output parameters of $q(h|v)$ given $v$. Enables amortized inference — cost is one forward pass rather than iterative optimization. Foundation of VAEs.

### Logical Structure
Chapter 19 introduces the variational inference framework that underlies VAEs (Chapter 20, section 20.10.3) and connects to the ELBO objective used throughout modern generative modeling.

---

## Chapter 20: Deep Generative Models

### Core Argument
Deep generative models — including Boltzmann machines, deep belief networks, VAEs, and GANs — learn to represent complex data distributions and generate realistic samples; GANs avoid the need for approximate inference or partition function estimation through adversarial training, while VAEs use variational inference for tractable likelihood lower bounds.

### Key Concepts & Algorithms

**Boltzmann Machines:** Energy-based undirected model $P(x) = \exp(-E(x))/Z$ with energy $E(x) = -x^\top Ux - b^\top x$. When hidden units present: $E(v,h) = -v^\top Rv - v^\top Wh - h^\top Sh - b^\top v - c^\top h$. Learning rule is local (Hebbian): update depends only on statistics of connected units.

**Restricted Boltzmann Machines (RBMs):** Bipartite graph (no within-layer connections). Factorial conditional distributions: $P(h_j=1|v) = \sigma(c_j + W_{:,j}^\top v)$. Enables efficient Gibbs sampling. Partition function intractable (proved by Long and Servedio, 2010). Trained with CD or SML.

**Deep Belief Networks (DBNs) (Hinton et al., 2006):** Hybrid model: undirected connections at top layers, directed connections pointing down. Multiple layers of latent variables. Trained greedily by stacking RBMs. Key historical contribution: showed deep networks could be trained without backprop. Now largely superseded.

**Deep Boltzmann Machines (DBMs) (Salakhutdinov and Hinton, 2009):** Fully undirected model with multiple hidden layers. Requires doubly counting weights from adjacent RBMs during greedy pretraining. Both inference and learning are intractable — require variational inference and MCMC.

**Variational Autoencoders (VAEs) (Kingma and Welling, 2013; Rezende et al., 2014):** Directed latent variable model $p_{model}(z, x) = p_{model}(z)p_{model}(x|z)$. Generator network parametrizes $p_{model}(x|z)$. Inference network (encoder) $q(z|x)$ approximates posterior. 

ELBO objective: $\mathcal{L}(q) = E_{z \sim q(z|x)}[\log p_{model}(z, x)] + H(q(z|x)) = E_{z \sim q(z|x)}[\log p_{model}(x|z)] - D_{KL}(q(z|x) \| p_{model}(z)) \leq \log p_{model}(x)$

Training: maximize ELBO with backpropagation. Reparametrization trick: $z = \mu + \sigma \odot \epsilon$ where $\epsilon \sim \mathcal{N}(0,I)$ — enables gradients to flow through sampling operation. 

Properties: smooth latent space (interpolation produces realistic samples); samples from VAEs tend to be blurry (MSE reconstruction loss averages modes); uses only small subset of latent dimensions in practice.

**Generative Adversarial Networks (GANs) (Goodfellow et al., 2014):** Two networks trained adversarially:
- Generator $g(z;\theta^{(g)})$: maps noise $z$ to data samples
- Discriminator $d(x;\theta^{(d)})$: outputs probability that $x$ is real data

Zero-sum game: $v(\theta^{(g)}, \theta^{(d)}) = E_{x \sim p_{data}}[\log d(x)] + E_{x \sim p_{model}}[\log(1 - d(x))]$

Generator minimizes, discriminator maximizes. At convergence: $d(x) = 1/2$ everywhere, generator distribution matches data distribution.

Key properties:
- No partition function or approximate inference needed
- Produces sharper samples than VAEs
- Training can be unstable: non-convergence problem, mode collapse
- Discriminator must use dropout for stable training
- Practical best formulation: generator maximizes $\log d(x)$ (not minimizes $\log(1 - d(x))$) — avoids vanishing gradients early in training

DCGAN (Radford et al., 2015): Deep convolutional GAN; stabilizes GAN training for image synthesis. LAPGAN (Denton et al., 2015): hierarchical GAN producing images from coarse to fine.

**Generative Moment Matching Networks:** Minimize Maximum Mean Discrepancy (MMD) between generated and real samples. Works but produces blurrier samples than GANs.

**Auto-Regressive Networks:** $p(x) = \prod_i p(x_i | x_{i-1},...,x_1)$. Each conditional parametrized by neural network. PixelRNN, PixelCNN for image generation. Fully visible Bayes networks. No latent variables.

**NADE (Neural Autoregressive Density Estimator):** Efficient auto-regressive model with parameter sharing across conditionals.

**Sampling from Autoencoders:** Multiple approaches: Markov chain on autoencoder outputs; generative stochastic networks; using DAE's estimated score function for MCMC.

**Evaluating Generative Models:** Parzen window / kernel density estimation for approximating log-likelihood. AIS for exact log-likelihood bounds. Inception score, FID score (not yet standard in 2016). Human evaluation (perceptual quality). No single metric captures all desired properties.

### Key Results & Benchmarks
- DBNs (2006): outperformed SVMs on MNIST — key result that launched deep learning renaissance
- VAEs: smooth latent space, reasonable samples but blurry
- GANs (2014): sharper samples than VAEs, but harder to train; no mode collapse in ideal case
- DCGAN (2015): stable GAN training for room images, learned structured latent space
- LAPGAN: 40% of generated images fooled human observers on bedroom dataset

### Logical Structure
Chapter 20 unifies all the methods of Part III into a comparative taxonomy of deep generative models. GANs and VAEs represent the two most practically important approaches.

### Notable Quotes
> "Generative adversarial networks are based on a game theoretic scenario in which the generator network must compete against an adversary." — p.699

### Cross-Chapter Connections
Builds on variational inference (Chapter 19), undirected models (Chapters 16-18), autoencoders (Chapter 14), and RNNs (Chapter 10). GANs introduced here are the foundation for modern image synthesis, video generation, and data augmentation.

---

## Master Concept Index

**Adam optimizer** — Adaptive learning rate algorithm combining momentum and RMSProp with bias correction. Ch. 8.

**AdaGrad** — Per-parameter adaptive learning rate using cumulative squared gradient history. Ch. 8.

**Adversarial examples** — Inputs specifically designed to cause misclassification by adding imperceptible perturbations. Ch. 7.

**Attention mechanism** — Weighted average of encoder hidden states, enabling decoder to selectively focus on relevant input parts. Ch. 10, 12.

**Autoencoder** — Neural network trained to encode input to lower-dimensional representation then reconstruct it. Ch. 14.

**Back-propagation** — Algorithm for computing gradients in neural networks using chain rule in reverse through computational graph. Time O(n) in graph edges. Ch. 6.

**Batch normalization** — Normalizes activations within a minibatch; reduces covariate shift, acts as regularizer. Ch. 7, 8.

**Bayes' Rule** — $P(x|y) = P(x)P(y|x)/P(y)$. Ch. 3.

**Boltzmann machine** — Energy-based undirected probabilistic model with visible and hidden units. Ch. 20.

**BPTT (Back-propagation through time)** — Applying back-propagation to unfolded RNN. O(τ) cost. Ch. 10.

**Capacity** — Model's ability to fit a wide variety of functions. Ch. 5.

**Chain rule** — $\frac{\partial z}{\partial x} = \frac{\partial z}{\partial y}\frac{\partial y}{\partial x}$. Fundamental to back-propagation. Ch. 4, 6.

**Cliffs and exploding gradients** — Steep regions from multiplying many large weights. Solution: gradient clipping. Ch. 8, 10.

**Conditional probability** — $P(y|x) = P(x,y)/P(x)$. Ch. 3.

**Connectionism** — 1980s-1990s movement emphasizing distributed processing in neural-like networks. Ch. 1.

**Contrastive divergence (CD)** — Approximates negative phase of Boltzmann machine learning by running k MCMC steps from data. Ch. 18.

**Convolution** — Linear operation $S(i,j) = \sum_m\sum_n I(i-m,j-n)K(m,n)$. Core operation of CNNs. Ch. 9.

**Cross-entropy** — $H(P,Q) = -E_x[\log Q(x)]$. Used as cost function for classification. Ch. 3, 6.

**Curse of dimensionality** — Problems become exponentially harder in high-dimensional spaces. Ch. 5.

**Dataset augmentation** — Creating additional training examples via class-preserving transformations. Ch. 7.

**Deep Belief Network (DBN)** — Hybrid directed/undirected multi-layer generative model. Key to 2006 deep learning revival. Ch. 20.

**Deep Boltzmann Machine (DBM)** — Fully undirected multi-layer model. Requires variational inference + MCMC. Ch. 20.

**Distributed representation** — Each input represented by many features; each feature active for many inputs. Exponentially efficient. Ch. 1, 15.

**Dropout** — Randomly zeroing units during training (probability 0.5 for hidden units). Trains exponential ensemble sharing parameters. Ch. 7.

**Early stopping** — Halt training when validation error begins rising. Equivalent to L2 regularization under some conditions. Ch. 7.

**Echo state networks (ESNs)** — Fixed recurrent weights set to preserve dynamics; only learn output weights. Reservoir computing. Ch. 10.

**Eigendecomposition** — $A = V\text{diag}(\lambda)V^{-1}$. Decomposes matrix into eigenvectors and eigenvalues. Ch. 2.

**Empirical risk minimization** — Minimize average loss on training set as proxy for true risk. Ch. 8.

**Encoder-decoder** — Architecture with encoder RNN compressing input to context vector; decoder RNN generating output sequence. Ch. 10.

**Energy-based model** — $P(x) = \exp(-E(x))/Z$. Lower energy = higher probability. Ch. 16.

**Expectation** — $E_x[f(x)] = \sum_x P(x)f(x)$ or $\int p(x)f(x)dx$. Ch. 3.

**Expectation maximization (EM)** — Iterative two-step optimization: E-step infers latent variables, M-step updates parameters. Ch. 19.

**Factor analysis** — Linear factor model with diagonal noise covariance. Ch. 13.

**Frobenius norm** — $\|A\|_F = \sqrt{\sum_{i,j} A_{i,j}^2}$. Matrix analog of L2 vector norm. Ch. 2.

**GAN (Generative Adversarial Network)** — Two-network adversarial game: generator creates samples, discriminator distinguishes real from fake. Ch. 20.

**Gaussian distribution** — $\mathcal{N}(x;\mu,\sigma^2)$. Normal distribution. Most common assumption for continuous data. Ch. 3.

**Gibbs sampling** — MCMC method sampling each variable conditioned on others. Efficient for RBMs. Ch. 17.

**Glorot/Xavier initialization** — $W_{i,j} \sim U(-\sqrt{6/(m+n)}, \sqrt{6/(m+n)})$. Balances gradient and activation variance. Ch. 8.

**Gradient clipping** — Rescale gradient when norm exceeds threshold: $g \leftarrow g \cdot v/\|g\|$. Prevents exploding gradients in RNNs. Ch. 8, 10.

**GRU (Gated Recurrent Unit)** — Simplified LSTM with update gate and reset gate. Comparable performance to LSTM. Ch. 10.

**Hessian matrix** — $H_{i,j} = \partial^2 f/\partial x_i \partial x_j$. Matrix of second-order partial derivatives. Positive definite at minimum. Ch. 4.

**Hyperparameters** — Parameters not learned by training algorithm itself; selected using validation set. Ch. 5.

**ICA (Independent Component Analysis)** — Finds statistically independent latent factors. Requires non-Gaussian priors. Cocktail party problem. Ch. 13.

**Ill-conditioning** — High condition number of Hessian causes gradient descent to make slow progress. Ch. 8.

**Importance sampling** — Estimate $E_p[f]$ by sampling from proposal $q$ and reweighting. Ch. 17.

**Jacobian matrix** — $J_{i,j} = \partial f(x)_i/\partial x_j$. Matrix of first-order partial derivatives for vector-valued functions. Ch. 4.

**KKT conditions** — Karush-Kuhn-Tucker optimality conditions for constrained optimization. Ch. 4.

**KL divergence** — $D_{KL}(P\|Q) = E_x[\log P(x)/Q(x)]$. Asymmetric measure of distribution difference. Always ≥ 0. Ch. 3.

**Kernel trick** — Implicitly map inputs to high-dimensional space using kernel function $K(x,x') = \phi(x)^\top\phi(x')$. Ch. 5.

**L1 regularization** — $\Omega(\theta) = \|w\|_1$. Promotes sparse weights. Equivalent to Laplace prior. Ch. 7.

**L2 regularization (weight decay)** — $\Omega(\theta) = \frac{1}{2}\|w\|_2^2$. Shrinks weights. Equivalent to Gaussian prior. Ch. 7.

**Latent variable** — Unobserved variable in a probabilistic model. Enriches model expressiveness. Ch. 3.

**Leaky ReLU** — $g(z) = \max\{\alpha z, z\}$. Allows small gradient for negative inputs. Ch. 6.

**Leaky units** — RNN hidden units with linear self-connections near 1.0; implement running average. Ch. 10.

**LeNet** — First successful deep CNN for digit recognition (LeCun et al., 1998). Ch. 9.

**LSTM (Long Short-Term Memory)** — Gated RNN with cell state, forget gate, input gate, output gate. Hochreiter and Schmidhuber (1997). Ch. 10.

**Manifold hypothesis** — Real-world data lies on low-dimensional manifolds in high-dimensional ambient space. Ch. 5.

**Markov Chain Monte Carlo (MCMC)** — Sampling method using Markov chain with target distribution as stationary distribution. Ch. 17.

**Maximum likelihood estimation (MLE)** — $\theta_{ML} = \arg\max_\theta \sum_i \log p_{model}(x^{(i)};\theta)$. Minimizes KL divergence from data to model. Ch. 5.

**Maxout unit** — $g_i(z) = \max_{j\in[k]} z_{i,j}$. Can approximate any convex function. Ch. 6.

**Mean field approximation** — Approximate posterior as fully factorized: $q(h|v) = \prod_i q(h_i|v_i)$. Ch. 19.

**Minibatch SGD** — Use small random subset of training data to estimate gradient. Enables learning from huge datasets. Ch. 5, 8.

**MLP (Multilayer Perceptron)** — Feedforward network with multiple hidden layers. Quintessential deep learning model. Ch. 6.

**Momentum** — Accumulate exponentially decaying moving average of gradient; continue in that direction. Terminal velocity $\|g\|/(1-\alpha)$. Ch. 8.

**Moore-Penrose pseudoinverse** — $A^+ = VD^+U^\top$. Solves least-squares minimization. Ch. 2.

**Multi-task learning** — Train multiple tasks simultaneously with shared lower layers. Ch. 7.

**Natural gradient** — Follows steepest descent in probability distribution space rather than parameter space. Ch. 8.

**Nesterov momentum** — Evaluates gradient at anticipated future position. Improves convex batch convergence from $O(1/k)$ to $O(1/k^2)$. Ch. 8.

**Neural language model (Bengio et al., 2001)** — Neural network predicting next word; learns distributed word representations. Ch. 12.

**Newton's method** — $\theta^* = \theta - H^{-1}\nabla_\theta J(\theta)$. Second-order optimization. Attracted to saddle points; not practical for large networks. Ch. 4, 8.

**Noise-contrastive estimation (NCE)** — Distinguishes data from noise distribution; estimates partition function as parameter. Ch. 18.

**n-gram model** — Language model based on fixed-length token sequences. High capacity, limited generalization. Ch. 12.

**Orthogonal initialization** — Initialize weight matrices as orthogonal matrices. Preserves gradient norm through layers. Ch. 8.

**Overfitting** — Large gap between training and test error. Model too complex for amount of data. Ch. 5.

**Parameter sharing** — Using same parameter for multiple functions. Key to CNNs (spatial) and RNNs (temporal). Ch. 9, 10.

**Partition function** — $Z = \sum_x \exp(-E(x))$. Normalization constant for undirected models. Generally intractable. Ch. 16, 18.

**PCA (Principal Components Analysis)** — Linear dimensionality reduction finding directions of maximum variance. Ch. 2, 13.

**Perceptron** — First learning algorithm for binary classification (Rosenblatt, 1958). Cannot learn XOR. Ch. 1.

**Pooling** — Summarizes local neighborhoods in feature maps. Max pooling, average pooling. Provides translation invariance. Ch. 9.

**Prior distribution** — $p(\theta)$: probability distribution over parameters before observing data. Ch. 3.

**Pseudolikelihood** — Approximate joint likelihood with product of conditionals. Consistent but less efficient than MLE. Ch. 18.

**Random search** — Sample hyperparameters randomly from distributions. More efficient than grid search (Bergstra and Bengio, 2012). Ch. 11.

**RBM (Restricted Boltzmann Machine)** — Undirected bipartite graph with visible and hidden units. Factorial conditionals. Key building block of deep generative models. Ch. 16, 20.

**ReLU (Rectified Linear Unit)** — $g(z) = \max\{0, z\}$. Current default hidden unit activation. Ch. 6.

**Representation learning** — Learning the transformation from data to a more useful representation. Ch. 1, 15.

**Reparametrization trick** — $z = \mu + \sigma \odot \epsilon$ allows backpropagation through sampling. Key to VAE training. Ch. 20.

**Reservoir computing** — Computing paradigm where random fixed recurrent connections create a rich state space; only readout layer is trained. Ch. 10.

**RMSProp (Hinton, 2012)** — Adaptive learning rate using exponentially decaying average of squared gradients. Ch. 8.

**RNN (Recurrent Neural Network)** — Neural network with hidden-to-hidden connections enabling sequence processing. Parameter sharing across time. Ch. 10.

**Saddle points** — Points where gradient vanishes but Hessian is indefinite. More common than local minima in high-dimensional spaces. Ch. 8.

**Score function** — $\nabla_x \log p(x)$. Gradient of log-density. Denoising autoencoders estimate the score function. Ch. 14.

**Score matching** — Train to match score of data distribution. Avoids partition function. Ch. 18.

**Semi-supervised learning** — Using both labeled and unlabeled data for supervised tasks. Ch. 7.

**SGD (Stochastic Gradient Descent)** — Update parameters using gradient estimated from small random minibatch. Core training algorithm for deep learning. Ch. 5, 8.

**Sigmoid** — $\sigma(x) = 1/(1+\exp(-x))$. Squashes to (0,1). Used for binary output. Ch. 3, 6.

**Slow Feature Analysis (SFA)** — Finds slowly varying features in time sequences. Learns features resembling V1 complex cells. Ch. 13.

**Softmax** — $\text{softmax}(z)_i = \exp(z_i)/\sum_j \exp(z_j)$. Probability distribution over discrete outputs. Ch. 3, 6.

**Sparse coding** — Representation where most elements are zero. Alternates between inference and dictionary learning. Ch. 13.

**Stochastic maximum likelihood (SML) / Persistent CD** — Maintains persistent MCMC chain for training undirected models. Ch. 18.

**SVD (Singular Value Decomposition)** — $A = UDV^\top$. Generalizes eigendecomposition to non-square matrices. Ch. 2.

**tanh** — Hyperbolic tangent activation. Saturates but symmetric around zero. Ch. 6.

**Teacher forcing** — Use ground truth $y^{(t)}$ as next RNN input during training. Enables parallelization. Ch. 10.

**Transfer learning** — Apply knowledge learned in one context to another related context. Ch. 15.

**Universal approximation theorem** — Single hidden layer feedforward network of sufficient width can approximate any continuous function. Hornik et al. (1989). Ch. 6.

**Undercomplete autoencoder** — Code dimension less than input. Forces compression. Learns PCA subspace if linear. Ch. 14.

**VAE (Variational Autoencoder)** — Directed generative model trained by maximizing ELBO using recognition network. Smooth latent space. Ch. 20.

**Vanishing gradients** — Gradients become exponentially small as they propagate through many layers or time steps. Critical problem for RNNs. Ch. 8, 10.

**Variational inference** — Approximate inference by optimizing over tractable family of distributions. Ch. 19.

**VGGNet** — Very deep CNNs (16-19 layers) with small (3×3) kernels. Ch. 9, 12.

**Vocabulary softmax** — Output distribution over vocabulary. Computationally expensive for large vocabularies. Ch. 12.

**Weight decay** — L2 regularization; adds $\lambda\|w\|_2^2$ penalty to objective. Ch. 7.

**Weight initialization** — Critical for training. Must break symmetry. Glorot/Xavier initialization commonly used. Ch. 8.

**Word embeddings** — Dense distributed representations of words. Encode semantic similarity. Bengio et al. (2001). Ch. 12, 15.

**XOR problem** — Classic example showing need for hidden layers. Linear model cannot solve it; single-layer ReLU network can. Ch. 6.
