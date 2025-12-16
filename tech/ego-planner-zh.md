arXiv:2008.08835v2 [cs.RO] 2020年12月7日
IEEE 机器人与自动化快报。预印本。2020年10月接受
# EGO-Planner：一种用于四旋翼飞行器的无ESDF基于梯度的局部规划器
Xin Zhou, Zhepei Wang, Hongkai Ye, Chao Xu and Fei Gao
摘要—基于梯度的规划器广泛应用于四旋翼飞行器的局部规划中，其中欧几里得符号距离场（ESDF）对于评估梯度的大小和方向至关重要。然而，计算这样一个场存在大量冗余，因为轨迹优化过程仅覆盖了ESDF更新范围中非常有限的子空间。本文提出了一种无ESDF的基于梯度的规划框架，显著减少了计算时间。主要的改进在于，惩罚函数中的碰撞项是通过将碰撞轨迹与无碰撞引导路径进行比较来制定的。由此产生的障碍物信息仅在轨迹碰到新障碍物时才会被存储，使得规划器仅提取必要的障碍物信息。然后，如果违反了动力学可行性，我们会延长分配的时间。引入了一种各向异性曲线拟合算法，在保持原始形状的同时调整轨迹的高阶导数。基准比较和真实世界实验验证了其鲁棒性和高性能。源代码已作为ROS包发布。
索引词—运动与路径规划；自动驾驶车辆导航；空中系统：应用
# I. 引言
近年来，四旋翼飞行器在线规划方法的出现极大地推动了空中自主性的边界，使得无人机飞出实验室并出现在众多现实世界的应用中。在这些方法中，基于梯度的方法（平滑轨迹并利用梯度信息提高其安全性）显示出巨大的潜力并越来越受欢迎 [1]。
传统上，基于梯度的规划器依赖于预先构建的ESDF地图来评估梯度的大小和方向，并使用数值优化来生成局部最优解。虽然优化程序享有快速收敛的优势，但它们在预先构建所需的ESDF方面深受其苦。正如统计数据（EwOK [2] 中的表II）所述，ESDF计算占据了进行局部规划总处理时间的约 $70\%$。因此，我们可以肯定地宣称，构建ESDF已成为基于梯度的规划器的瓶颈，阻碍了该方法应用于资源受限的平台。
手稿接收日期：2020年8月19日；接受日期：2020年10月21日。本文由编辑Nancy Amato在评估副编辑和审稿人的意见后推荐发表。本工作得到了中央高校基本科研业务费专项资金的支持，资助号为2020QNA5013。（通讯作者：Fei Gao。）
所有作者均来自浙江大学工业控制技术国家重点实验室和网络系统与控制研究所，杭州，310027，中国。{iszhouxin, wangzhepei, hkye, cxu, and fgaoaa}@zju.edu.cn
数字对象标识符 (DOI)：见本页顶部。
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/eded2acd0e880d1c6b5776c79cb6cd1c26e1c55111be788a5a7914a190661c89.jpg)


图 1：优化过程中的轨迹仅覆盖了ESDF更新范围中非常有限的空间。

尽管ESDF被广泛使用，但很少有工作分析其必要性。通常，构建ESDF有两种方法。如第二节详述，方法可分为增量全局更新 [3] 和批量局部计算 [4]。然而，它们都没有关注轨迹本身。因此，太多的计算花费在计算对规划没有贡献的ESDF值上。换句话说，当前的基于ESDF的方法并不单独且直接地服务于轨迹优化。如图1所示，对于一般的自主导航场景，无人机需要在局部避免碰撞，轨迹仅覆盖了ESDF更新范围的有限空间。在实践中，虽然一些手工规则可以决定一个较小的ESDF范围，但它们缺乏理论合理性，仍然会导致不必要的计算。
在本文中，我们设计了一种名为EGO的无ESDF基于梯度的局部规划框架，并结合了细致的工程考虑使其轻量且鲁棒。所提出的算法由基于梯度的样条优化器和后细化过程组成。首先，我们通过平滑性、碰撞和动力学可行性项来优化轨迹。与查询预计算ESDF的传统方法不同，我们通过将障碍物内的轨迹与引导的无碰撞路径进行比较来建模碰撞成本。然后我们将力投影到碰撞轨迹上并生成估计梯度以将轨迹包裹出障碍物。在优化过程中，轨迹会在附近的障碍物之间反弹几次，最终终止在安全区域。通过这种方式，我们仅在必要时计算梯度，并避免在与局部轨迹无关的区域计算ESDF。如果生成的轨迹违反了动力学限制，这通常是由不合理的时间分配引起的，

IEEE 机器人与自动化快报。预印本。2020年10月接受
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/e6782f502b31d23a6f4aff065deaf94196ca7373c0a5e10c8467d07d2ae924b6.jpg)


图 2：轨迹陷入局部极小值，这非常常见，因为相机无法看到障碍物的背面。

则激活细化过程。在细化过程中，当超过限制时，重新分配轨迹时间。随着时间分配的增加，生成一个新的B样条，该样条拟合先前的动力学不可行样条，同时平衡可行性和拟合精度。为了提高鲁棒性，拟合精度被各向异性地建模，在轴向和径向方向上具有不同的惩罚。
据我们所知，该方法是第一个在没有ESDF的情况下实现基于梯度的局部规划的方法。与现有的最先进工作相比，所提出的方法生成的安全轨迹具有相当的平滑性和激进性，但通过省略ESDF维护，计算时间降低了一个数量级以上。我们在仿真和真实世界中进行了全面的测试以验证我们的方法。这封信的贡献是：
1) 我们提出了一种新颖且鲁棒的基于梯度的四旋翼局部规划方法，该方法直接从障碍物而不是预构建的ESDF评估和投影梯度信息。
2) 我们提出了一种轻量级但有效的轨迹细化算法，通过用各向异性误差惩罚制定轨迹拟合问题来生成更平滑的轨迹。
3) 我们将所提出的方法集成到一个完全自主的四旋翼系统中，并发布我们的软件供社区参考<sup>1</sup>。
# II. 相关工作
# A. 基于梯度的运动规划
基于梯度的运动规划是无人机局部轨迹生成的主流方法，它将问题表述为无约束非线性优化。ESDF最早由Ratliff等人 [5] 引入机器人运动规划中。利用其丰富的梯度信息，许多规划框架直接在配置空间中优化轨迹。然而，在离散时间 [5, 6] 中优化轨迹并不适合无人机，因为它对动力学约束更为敏感。因此，[7] 提出了一种用于无人机规划的连续时间多项式轨迹优化方法。然而，涉及的势函数积分导致了沉重的计算负担。此外，即使随机重启，该方法的成功率也仅在 $70\%$ 左右。针对这些缺点，[2] 引入了轨迹的B样条参数化

算法 1 检查并添加障碍物信息 (CheckAndAddObstacleInfo)

1: 符号：环境 $\mathcal{E}$，控制点结构 Q，锚点 p，排斥方向向量 v，碰撞段 S
2: 输入：$\mathcal{E}$，Q
3: for Q 中的 $\mathbf{Q}_i$ do
4: if FindConsecutiveCollidingSegment(Q) then
5: S.push_back(GetCollisionSegment())
6: end if
7: end for
8: for S 中的 $\mathbf{S}_i$ do
9: $\Gamma \leftarrow$ PathSearch(E, Si)
10: for $\mathbf{S}_i$.begin $\leq j\leq \mathbf{S}_i$.end do
11: $\{\mathbf{p},\mathbf{v}\} \gets$ Find_p_v_Pairs(Qj,Γ)
12: Qj.push_back({p,v})
13: end for
14: end for
这充分利用了凸包性质。在 [8] 中，通过前端寻找无碰撞初始路径，成功率显著提高。此外，当初始无碰撞路径的生成考虑到动力学约束时，性能进一步提高 [9, 10]。Zhou等人 [11] 结合感知意识使系统更加鲁棒。在上述方法中，ESDF在评估到附近障碍物的距离以及梯度大小和方向方面起着至关重要的作用。
# B. 欧几里得符号距离场 (ESDF)
ESDF长期以来一直用于从嘈杂的传感器数据构建对象，已有二十多年的历史 [12]，并自 [5] 以来重新引起了机器人运动规划的兴趣。Felzenszwalb等人 [4] 提出了一种包络算法，将ESDF构建的时间复杂度降低到 $O(n)$，其中 $n$ 表示体素数量。该算法不适合ESDF的增量构建，而四旋翼飞行过程中通常需要动态更新场。为了解决这个问题，Oleynikova [13] 和 Han [3] 提出了增量ESDF生成方法，即Voxblox和FIESTA。虽然这些方法在动态更新情况下非常高效，但生成的ESDF几乎总是包含冗余信息，这些信息可能根本不会在规划过程中使用。如图1所示，该轨迹仅扫过整个ESDF更新范围中非常有限的子空间。因此，设计一种更智能、更轻量的方法，而不是维护整个场，是有价值的。
# III. 避障力估计
在本文中，决策变量是B样条曲线的控制点 $\mathbf{Q}$。每个 $\mathbf{Q}$ 独立拥有自己的环境信息。最初，给出一个满足终端约束的朴素B样条曲线 $\Phi$，不考虑碰撞。然后，优化过程开始。对于在迭代中检测到的每个碰撞段，生成一条无碰撞路径 $\Gamma$。碰撞段的每个控制点 $\mathbf{Q}_i$，
2
<sup>1</sup>https://github.com/ZJU-FAST-Lab/ego-planner
ZHOU et al.: EGO-PLANNER: AN ESDF-FREE GRADIENT-BASED LOCAL PLANNER FOR QUADROTORS
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/c95991a2065c918495bffbd94857dcc4c9fc47930a2b6dcae7140dd887f18898.jpg)


(a) $\{\mathbf{p},\mathbf{v}\}$ 对

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/199ba46cbb8568d8377b09cdcfe341272e0f9d1857ef7898d30e64f8b3f06c47.jpg)


(b) $\mathbf{p},\mathbf{v}$ 生成

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/147102c274c77af015f53cff350a07a1322a16d9507e35aeaa57215c5562bde6.jpg)


(c) 一个 $\{\mathbf{p},\mathbf{v}\}$ 对的距离场


图 3：a) 穿过障碍物的轨迹 $\Phi$ 为控制点生成若干 $\{\mathbf{p},\mathbf{v}\}$ 对。$\mathbf{p}$ 是障碍物表面的点，$\mathbf{v}$ 是从控制点指向 $\mathbf{p}$ 的单位向量。b) 垂直于切向量 $\mathbf{R}_i$ 的平面 $\Psi$ 与 $\Gamma$ 相交形成一条线 $l$，从中确定一个 $\{\mathbf{p},\mathbf{v}\}$ 对。c) 距离场定义 $d_{ij} = (\mathbf{Q}_i - \mathbf{p}_{ij})\cdot \mathbf{v}_{ij}$ 的切片可视化。颜色表示距离，箭头是等于 $\mathbf{v}$ 的相同梯度。$\mathbf{p}$ 位于零距离平面。

之后，将被分配一个位于障碍物表面的锚点 $\mathbf{p}_{ij}$ 和相应的排斥方向向量 $\mathbf{v}_{ij}$，如图3a所示。用 $i\in \mathbb{N}_+$ 表示控制点的索引，$j\in \mathbb{N}$ 表示 $\{\mathbf{p},\mathbf{v}\}$ 对的索引。注意，每个 $\{\mathbf{p},\mathbf{v}\}$ 对仅属于一个特定的控制点。为简洁起见，我们在不引起歧义的情况下省略下标 $ij$。本文中详细的 $\{\mathbf{p},\mathbf{v}\}$ 对生成过程总结在算法1中，并如图3b所示。然后，从 $\mathbf{Q}_i$ 到第 $j^{th}$ 个障碍物的障碍物距离定义为
$$
d _ {i j} = \left(\mathbf {Q} _ {i} - \mathbf {p} _ {i j}\right) \cdot \mathbf {v} _ {i j}. \tag {1}
$$
为了避免在轨迹逃离当前障碍物之前的前几次迭代中重复生成 $\{\mathbf{p},\mathbf{v}\}$ 对，我们采用一个标准，即只有当当前 $\mathbf{Q}_i$ 满足所有有效 $j$ 的 $d_{ij} > 0$ 时，才认为控制点 $\mathbf{Q}_i$ 所在的障碍物是新发现的。此外，该标准允许仅将有助于最终轨迹的必要障碍物纳入优化。因此，操作时间显著减少。
为了将必要的环境意识纳入局部规划器，我们需要显式构建一个目标函数，使轨迹远离障碍物。ESDF提供了这种至关重要的碰撞信息，但代价是沉重的计算负担。此外，如图2所示，基于ESDF的规划器很容易陷入局部极小值并无法逃离障碍物，这是由于ESDF信息不足甚至错误造成的。为了避免这种情况，总是需要额外的前端来提供无碰撞的初始轨迹。上述方法在提供避障的关键信息方面优于ESDF，因为显式设计的排斥力对于各种任务和环境都相当有效。此外，所提出的方法不需要无碰撞初始化。
# IV. 基于梯度的轨迹优化
# A. 问题表述
在本文中，轨迹由均匀B样条曲线 $\Phi$ 参数化，该曲线由其阶数
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/cb288e711d40f21bff195f2f3d0907b238c718523a621683555bf4752b2a6a8e.jpg)


图 4：B样条曲线的凸包性质。灰点表示控制点。只要所有控制点都在可行性边界框（黑色虚线框）内，整条曲线就保持在该框内。不失一般性，每个凸包由四个顶点组成。

$p_b$，$N_c$ 个控制点 $\{\mathbf{Q}_1, \mathbf{Q}_2, \dots, \mathbf{Q}_{N_c}\}$ 和一个节点向量 $\{t_1, t_2, \dots, t_M\}$ 唯一确定，其中 $\mathbf{Q}_i \in \mathbb{R}^3$，$t_m \in \mathbb{R}$ 且 $M = N_c + p_b$。为了简化和提高轨迹评估的效率，我们方法中使用的B样条是均匀的，这意味着每个节点与其前一个节点的时间间隔 $\triangle t = t_{m+1} - t_m$ 相同。本文的问题表述基于当前最先进的四旋翼局部规划框架 Fast-Planner [14]。
B样条具有凸包性质。该性质表明，B样条曲线的单个跨度仅由 $p_b + 1$ 个连续控制点控制，并位于这些点的凸包内。例如，$(t_i, t_{i+1})$ 内的跨度位于由 $\{\mathbf{Q}_{i-p_b}, \mathbf{Q}_{i-p_b+1}, \dots, \mathbf{Q}_i\}$ 形成的凸包内。另一个性质是，B样条的 $k^{th}$ 阶导数仍然是阶数为 $p_{b,k} = p_b - k$ 的B样条。由于 $\triangle t$ 沿 $\Phi$ 是相同的，速度 $\mathbf{V}_i$、加速度 $\mathbf{A}_i$ 和加加速度 $\mathbf{J}_i$ 曲线的控制点通过以下方式获得
$$
\mathbf {V} _ {i} = \frac {\mathbf {Q} _ {i + 1} - \mathbf {Q} _ {i}}{\triangle t}, \quad \mathbf {A} _ {i} = \frac {\mathbf {V} _ {i + 1} - \mathbf {V} _ {i}}{\triangle t}, \quad \mathbf {J} _ {i} = \frac {\mathbf {A} _ {i + 1} - \mathbf {A} _ {i}}{\triangle t}. \tag {2}
$$
我们遵循 [15] 的工作，在微分平坦输出的降维空间中规划控制点 $\mathbf{Q} \in \mathbb{R}^3$。

IEEE 机器人与自动化快报。预印本。2020年10月接受
优化问题表述如下：
$$
\min  _ {\mathbf {Q}} J = \lambda_ {s} J _ {s} + \lambda_ {c} J _ {c} + \lambda_ {d} J _ {d}, \tag {3}
$$
其中 $J_{s}$ 是平滑性惩罚，$J_{c}$ 是碰撞惩罚，$J_{d}$ 表示可行性。$\lambda_s, \lambda_c, \lambda_d$ 是每个惩罚项的权重。
1) 平滑性惩罚：在 [2] 中，平滑性惩罚被表述为轨迹导数平方（加速度、加加速度等）的时间积分。在 [10] 中，仅考虑轨迹的几何信息，而不考虑时间分配。在本文中，我们结合这两种方法，在不进行时间积分的情况下惩罚平方加速度和加加速度。
得益于凸包性质，最小化B样条轨迹的二阶和三阶导数的控制点足以减少整条曲线的这些导数。因此，平滑性惩罚函数表述为
$$
J _ {s} = \sum_ {i = 1} ^ {N _ {c} - 1} \| \mathbf {A} _ {i} \| _ {2} ^ {2} + \sum_ {i = 1} ^ {N _ {c} - 2} \| \mathbf {J} _ {i} \| _ {2} ^ {2}, \tag {4}
$$
这最小化了高阶导数，使整个轨迹平滑。
2) 碰撞惩罚：碰撞惩罚将控制点推离障碍物。这是通过采用安全间隙 $s_f$ 并惩罚 $d_{ij} < s_f$ 的控制点来实现的。为了进一步促进优化，我们构建了一个二阶连续可微的惩罚函数 $j_c$，并随着 $d_{ij}$ 的减小抑制其斜率，从而产生分段函数
$$
\begin{array}{c} j _ {c} (i, j) = \left\{ \begin{array}{l l} 0 & (c _ {i j} \leq 0) \\ c _ {i j} ^ {3} & (0 <   c _ {i j} \leq s _ {f}), \\ 3 s _ {f} c _ {i j} ^ {2} - 3 s _ {f} ^ {2} c _ {i j} + s _ {f} ^ {3} & (c _ {i j} > s _ {f}) \end{array} \right. \\ c _ {i j} = s _ {f} - d _ {i j}, \end{array} \tag {5}
$$
其中 $j_{c}(i,j)$ 是 $\{\mathbf{p},\mathbf{v}\}_{j}$ 对在 $\mathbf{Q}_i$ 上产生的成本值。每个 $\mathbf{Q}_i$ 上的成本是独立评估的，并从所有相应的 $\{\mathbf{p},\mathbf{v}\}_{j}$ 对累积。因此，如果一个控制点发现更多障碍物，它将获得更高的轨迹变形权重。具体来说，添加到第 $i^{th}$ 个控制点的成本值是 $j_{c}(\mathbf{Q}_{i}) = \sum_{j = 1}^{N_{p}}j_{c}(i,j)$，$N_{p}$ 是属于 $\mathbf{Q}_i$ 的 $\{\mathbf{p},\mathbf{v}\}_{j}$ 对的数量。结合所有 $\mathbf{Q}_i$ 上的成本得出总成本 $J_{c}$，即
$$
J _ {c} = \sum_ {i = 1} ^ {N _ {c}} j _ {c} \left(\mathbf {Q} _ {i}\right). \tag {6}
$$
与传统的基于ESDF的方法 [2, 10] 不同（它们通过场上的三线性插值计算梯度），我们通过直接计算 $J_{c}$ 对 $\mathbf{Q}_i$ 的导数来获得梯度，即
$$
\frac {\partial J _ {c}}{\partial \mathbf {Q} _ {i}} = \sum_ {i = 1} ^ {N _ {c}} \sum_ {j = 1} ^ {N _ {p}} \mathbf {v} _ {i j} \left\{ \begin{array}{l l} 0 & (c _ {i j} \leq 0) \\ - 3 c _ {i j} ^ {2} & (0 <   c _ {i j} \leq s _ {f}) \\ - 6 s _ {f} c _ {i j} + 3 s _ {f} ^ {2} & (c _ {i j} > s _ {f}) \end{array} . \right. \tag {7}
$$
3) 可行性惩罚：可行性通过限制轨迹在每个维度上的高阶导数来确保，即对所有 $t$ 应用 $|\Phi_r^{(k)}(t)| < \Phi_{r,\max}^{(k)}$，其中 $r \in \{x,y,z\}$ 表示每个维度。由于凸包性质，约束控制点的导数足以约束整个B样条。因此，惩罚函数表述为
$$
J _ {d} = \sum_ {i = 1} ^ {N _ {c}} w _ {v} F (\mathbf {V} _ {i}) + \sum_ {i = 1} ^ {N _ {c} - 1} w _ {a} F (\mathbf {A} _ {i}) + \sum_ {i = 1} ^ {N _ {c} - 2} w _ {j} F (\mathbf {J} _ {i}), \tag {8}
$$
其中 $w_{v}, w_{a}, w_{j}$ 是每个项的权重，$F(\cdot)$ 是控制点高阶导数的二阶连续可微度量函数。
$$
F (\mathbf {C}) = \sum_ {r = x, y, z} f \left(c _ {r}\right), \tag {9}
$$
$$
f \left(c _ {r}\right) = \left\{ \begin{array}{l l} a _ {1} c _ {r} ^ {2} + b _ {1} c _ {r} + c _ {1} & \left(c _ {r} \leq - c _ {j}\right) \\ \left(- \lambda c _ {m} - c _ {r}\right) ^ {3} & \left(- c _ {j} <   c _ {r} <   - \lambda c _ {m}\right) \\ 0 & \left(- \lambda c _ {m} \leq c _ {r} \leq \lambda c _ {m}\right), \\ \left(c _ {r} - \lambda c _ {m}\right) ^ {3} & \left(\lambda c _ {m} <   c _ {r} <   c _ {j}\right) \\ a _ {2} c _ {r} ^ {2} + b _ {2} c _ {r} + c _ {2} & \left(c _ {r} \geq c _ {j}\right) \end{array} \right. \tag {10}
$$
其中 $c_{r} \in \mathbf{C} \in \{\mathbf{V}_{i}, \mathbf{A}_{i}, \mathbf{J}_{i}\}$，$a_{1}, b_{1}, c_{1}, a_{2}, b_{2}, c_{2}$ 的选择满足二阶连续性，$c_{m}$ 是导数限制，$c_{j}$ 是二次区间和三次区间的分割点。$\lambda < 1 - \epsilon$ 是一个弹性系数，其中 $\epsilon \ll 1$，以使最终结果满足约束，因为成本函数是所有加权项的权衡。
# B. 数值优化
本文表述的问题具有两个方面的特点。首先，目标函数 $J$ 根据新发现的障碍物自适应地改变。这要求求解器能够快速重启。其次，二次项在目标函数的表述中占主导地位，使得 $J$ 近似为二次的。这意味着利用Hessian信息可以显著加速收敛。然而，在实时应用中获得精确的逆Hessian是禁止的，因为它消耗不可忽略的大量计算。为了规避这一点，采用了从梯度信息近似逆Hessian的拟牛顿法。
由于求解器的性能依赖于问题，我们比较了属于拟牛顿法的三种算法。它们是Barzilai-Borwein方法 [16]（能够以最粗略的Hessian估计快速重启）、截断牛顿法 [17]（通过向给定状态添加多个微小扰动来估计Hessian）、L-BFGS方法 [18]（从先前的目标函数评估中近似Hessian，但需要一系列迭代才能达到相对准确的估计）。第VI-B节的比较表明，L-BFGS在选择适当的内存大小时优于其他两种算法，平衡了重启的损失和逆Hessian估计的准确性。该算法简要解释如下。对于无约束

ZHOU et al.: EGO-PLANNER: AN ESDF-FREE GRADIENT-BASED LOCAL PLANNER FOR QUADROTORS
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/a80fb4421d8bc571de9fc990cf1cf661de3a58880f4ffe40471efda817288862.jpg)


图 5：优化轨迹 $\Phi_f$ 以拟合轨迹 $\Phi_s$，同时调整平滑性和可行性。黑点和绿点是轨迹上的采样点。$\Phi_f(\alpha T')$ 和 $\Phi_s(\alpha T)$ 之间的位移沿两个椭圆主轴分解为 $d_a$ 和 $d_r$。红色椭圆表面上的点产生相同的惩罚。

优化问题 $\min_{\mathbf{x} \in \mathbb{R}^n} f(\mathbf{x})$，$\mathbf{x}$ 的更新遵循近似牛顿步
$$
\mathbf {x} _ {k + 1} = \mathbf {x} _ {k} - \alpha_ {k} \mathbf {H} _ {k} \nabla \mathbf {f} _ {k}, \tag {11}
$$
其中 $\alpha_{k}$ 是步长，$\mathbf{H}_k$ 在每次迭代中通过以下公式更新
$$
\mathbf {H} _ {k + 1} = \mathbf {V} _ {k} ^ {T} \mathbf {H} _ {k} \mathbf {V} _ {k} + \rho_ {k} \mathbf {s} _ {k} \mathbf {s} _ {k} ^ {T}, \tag {12}
$$
其中 $\rho_{k} = (\mathbf{y}_{k}^{T}\mathbf{s}_{k})^{-1},\mathbf{V}_{k} = \mathbf{I} - \rho_{k}\mathbf{y}_{k}\mathbf{s}_{k}^{T},\mathbf{s}_{k} = \mathbf{x}_{k + 1} - \mathbf{x}_{k}$ 且 $\mathbf{y}_k = \nabla \mathbf{f}_{k + 1} - \nabla \mathbf{f}_k$
这里 $\mathbf{H}_k$ 不显式计算。该算法将 $\nabla \mathbf{f}_k$ 右乘到公式12并递归展开 $m$ 步，然后产生高效的双循环递归更新方法 [16]，导致线性时间/空间复杂度。Barzilai-Borwein步的权重用作L-BFGS更新的初始逆Hessian $\mathbf{H}_k^0$，即
$$
\mathbf {H} _ {k} ^ {0} = \frac {\mathbf {s} _ {k - 1} ^ {T} \mathbf {y} _ {k - 1}}{\mathbf {y} _ {k - 1} ^ {T} \mathbf {y} _ {k - 1}} \mathbf {I} \text {或} \frac {\mathbf {s} _ {k - 1} ^ {T} \mathbf {s} _ {k - 1}}{\mathbf {s} _ {k - 1} ^ {T} \mathbf {y} _ {k - 1}} \mathbf {I}. \tag {13}
$$
使用强Wolfe条件下的单调线搜索来强制收敛。
# V. 时间重分配与轨迹细化
在优化之前分配准确的时间分布是不合理的，因为规划器当时不知道最终轨迹的任何信息。因此，额外的时间重分配过程对于确保动力学可行性至关重要。以前的工作 [10, 19] 将轨迹参数化为非均匀B样条，并在某些段超过导数限制时迭代地延长节点跨度的子集。
然而，一个节点跨度 $\triangle t_{n}$ 影响多个控制点，反之亦然，导致在调整起始状态附近的节点跨度时，与先前轨迹的高阶不连续性。在本节中，根据IV中的安全轨迹 $\Phi_s$，通过合理的时间重分配重新生成均匀B样条轨迹 $\Phi_f$。然后，提出了一种各向异性曲线拟合方法，使 $\Phi_f$ 自由优化其控制点以满足高阶导数约束，同时保持与 $\Phi_s$ 几乎相同的形状。
首先，如Fast-Planner [14] 所做的那样，我们计算限制超出比率，
$$
r _ {e} = \max  \left\{\left| \mathbf {V} _ {i, r} / v _ {m} \right|, \sqrt {\left| \mathbf {A} _ {j , r} / a _ {m} \right|}, \sqrt [ 3 ]{\left| \mathbf {J} _ {k , r} / j _ {m} \right|}, 1 \right\}, \tag {14}
$$
其中 $i\in \{1,\dots ,N_c - 1\}$ $j\in \{1,\dots ,N_c - 2\}$ $k\in$ $\{1,\dots ,N_c - 3\}$ 且 $r\in \{x,y,z\}$ 轴。带有下标 $m$ 的符号表示导数的限制。$r_e$ 表示我们应该相对于 $\Phi_s$ 延长多少 $\Phi_f$ 的时间分配。注意，根据公式2，$\mathbf{V}_i, \mathbf{A}_j$ 和 $\mathbf{J}_k$ 分别与 $\triangle t$、$\triangle t$ 的平方和 $\triangle t$ 的立方成反比。然后我们获得 $\Phi_f$ 的新时间跨度
$$
\triangle t ^ {\prime} = r _ {e} \triangle t. \tag {15}
$$
通过求解闭式最小二乘问题，在边界约束下初始生成时间跨度为 $\triangle t'$ 的 $\Phi_f$，同时保持与 $\Phi_s$ 相同的形状和控制点数量。然后通过优化细化平滑性和可行性。由平滑性（第IV-A1节）、可行性（第IV-A3节）和曲线拟合（稍后介绍）的线性组合构成的惩罚函数 $J'$ 为
$$
\underset {\mathbf {Q}} {\min } J ^ {\prime} = \lambda_ {s} J _ {s} + \lambda_ {d} J _ {d} + \lambda_ {f} J _ {f}, \tag {16}
$$
其中 $\lambda_{f}$ 是拟合项的权重。
拟合惩罚函数 $J_{f}$ 表述为从点 $\Phi_f(\alpha T')$ 到相应 $\Phi_s(\alpha T)$ 的各向异性位移的积分，其中 $T$ 和 $T'$ 分别是 $\Phi_s$ 和 $\Phi_f$ 的轨迹持续时间，$\alpha \in [0,1]$。由于拟合曲线 $\Phi_s$ 已经是无碰撞的，我们为两条曲线的轴向位移分配低惩罚权重以放宽平滑性调整限制，并为径向位移分配高惩罚权重以避免碰撞。为了实现这一点，我们使用如图5所示的球体度量，使得同一球体表面上的位移产生相同的惩罚。我们用于 $\Phi_f(\alpha T')$ 的球体是通过将以 $\Phi_s(\alpha T)$ 为中心的椭圆绕其主轴之一（切线 $\Phi_s(\alpha T)$）旋转获得的。因此，轴向位移 $d_a$ 和径向位移 $d_r$ 可以通过以下方式计算
$$
\begin{array}{l} d _ {a} = (\Phi_ {f} - \Phi_ {s}) \cdot \frac {\dot {\Phi} _ {s}}{\| \dot {\Phi} _ {s} \|}, \\ d _ {r} = \left\| \left(\boldsymbol {\Phi} _ {f} - \boldsymbol {\Phi} _ {s}\right) \times \frac {\dot {\boldsymbol {\Phi}} _ {s}}{\| \dot {\boldsymbol {\Phi}} _ {s} \|} \right\|. \tag {17} \\ \end{array}
$$
拟合惩罚函数为
$$
J _ {f} = \int_ {0} ^ {1} \left[ \frac {d _ {a} \left(\alpha T ^ {\prime}\right) ^ {2}}{a ^ {2}} + \frac {d _ {r} \left(\alpha T ^ {\prime}\right) ^ {2}}{b ^ {2}} \right] \mathrm {d} \alpha , \tag {18}
$$
其中 $a$ 和 $b$ 分别是椭圆的半长轴和半短轴。该问题由L-BFGS求解。
# VI. 实验结果
# A. 实现细节
规划框架总结在算法2中。我们将B样条阶数设置为 $p_b = 3$。控制点数量 $N_c$ 在25左右变化，这由规划范围（约7m）和相邻点的初始距离间隔（约0.3m）决定。这些是平衡问题复杂性与自由度的经验参数。时间复杂度为 $O(N_c)$，因为根据B样条的局部支持性质，一个控制点仅影响附近的段。L-BFGS的复杂度在相同的相对容差下也是线性的。对于无碰撞路径搜索，我们采用 $\mathbf{A}^*$，它具有路径 $\Gamma$ 总是倾向于

算法 2 反弹规划 (Rebound Planning)

1: 符号：目标 $\mathcal{G}$，环境 $\mathcal{E}$，控制点结构 Q，惩罚 $J$ 梯度 G
2: 初始化：$\mathbf{Q}\gets$ FindInit(Qlast, $\mathcal{G}$)
3: while $\neg$ IsCollisionFree(E,Q) do
4: CheckAndAddObstacleInfo(E,Q)
5: $(J,\mathbf{G})\leftarrow$ EvaluatePenalty(Q)
6: $\mathbf{Q}\gets$ OneStepOptimize(J,G)
7: end while
8: if $\neg$ IsFeasible(Q) then
9: $\mathbf{Q}\gets$ ReAllocateTime(Q)
10: $\mathbf{Q}\gets$ CurveFittingOptimize(Q)
11: end if
12: return Q
自然接近障碍物表面的良好优势。因此，我们可以直接在 $\Gamma$ 上选择 $\mathbf{p}$ 而无需障碍物表面搜索。对于图3b中定义的向量 $\mathbf{R}_i$，可以通过均匀B样条参数化的性质推导出，$\mathbf{R}_i$ 满足
$$
\mathbf {R} _ {i} = \frac {\mathbf {Q} _ {i + 1} - \mathbf {Q} _ {i - 1}}{2 \triangle t}, \tag {19}
$$
这可以高效计算。公式18离散化为有限数量的点 $\Phi_f(k\triangle t')$ 和 $\Phi_s(k\triangle t)$，其中 $k \in \mathbb{N}, 0 \leq k \leq \lfloor T / \triangle t \rfloor$。为了进一步加强安全性，对最终轨迹周围固定半径的圆形管道进行碰撞检查，以提供足够的障碍物间隙。当未检测到碰撞时，优化器停止。真实世界实验在与 [19] 相同的飞行平台上进行，深度由 Intel RealSense D435² 获取。此外，我们修改了 Intel RealSense 的 ROS 驱动程序，使激光发射器每隔一帧闪烁一次。这允许设备在发射器的帮助下输出高质量的深度图像，以及不受激光干扰的双目图像。修改后的驱动程序也已开源。
# B. 优化算法比较
在本节中，讨论了三种不同的优化算法，包括 Barzilai-Borwein (BB) 方法、有限内存 BFGS (L-BFGS) 和截断牛顿 (T-NEWTON) 方法 [17]。具体来说，每种算法在随机地图中独立运行100次。所有相关参数，包括边界约束、时间分配、决策变量初始化和随机种子，对于不同的算法都设置为相同。记录了关于成功率、计算时间和目标函数评估次数的数据。由于失败案例中的数据没有意义，因此仅统计成功案例。相关结果如表I所示，表明L-BFGS显著优于其他两种算法。L-BFGS具有通过二阶泰勒展开进行近似的特点，适合优化第IV-B节中描述的目标函数。截断牛顿法也近似二阶优化方向 $\mathbf{H}^{-1}\nabla \mathbf{f}_k$。然而，过多的目标函数评估增加了优化时间。BB方法估计Hessian为标量 $\lambda$ 乘以 $\mathbf{I}$。然而，Hessian的估计不足仍然导致收敛速度低。

表 I：优化算法比较

<table><tr><td rowspan="2">算法</td><td rowspan="2">成功率</td><td colspan="3">时间(ms)</td><td colspan="3">函数评估</td></tr><tr><td>最小</td><td>平均</td><td>最大</td><td>最小</td><td>平均</td><td>最大</td></tr><tr><td>BB</td><td>0.86</td><td>0.21</td><td>0.50</td><td>1.14</td><td>108</td><td>268.2</td><td>508</td></tr><tr><td>T-NEWTON</td><td>0.62</td><td>0.3</td><td>0.79</td><td>3.59</td><td>109</td><td>344.29</td><td>702</td></tr><tr><td>L-BFGS</td><td>0.89</td><td>0.17</td><td>0.37</td><td>0.80</td><td>22</td><td>79.04</td><td>182</td></tr></table>

表 II：ESDF/无ESDF方法比较

<table><tr><td rowspan="2">方法</td><td rowspan="2">成功率</td><td rowspan="2">能量</td><td colspan="2">速度(m/s)</td><td colspan="3">时间(ms)</td></tr><tr><td>平均</td><td>最大</td><td>优化</td><td>ESDF</td><td>总计</td></tr><tr><td>EGO</td><td>0.89</td><td>49.92</td><td>2.12</td><td>2.24</td><td>0.37</td><td>/</td><td>0.37</td></tr><tr><td>ENI</td><td>0.69</td><td>35.55</td><td>2.09</td><td>2.23</td><td>0.43</td><td>5.03</td><td>5.46</td></tr><tr><td>EI</td><td>0.89</td><td>42.27</td><td>2.11</td><td>2.36</td><td>0.48</td><td>5.07</td><td>5.55</td></tr></table>


# C. 有无ESDF的轨迹生成
我们使用与第VI-B节相同的设置来进行此比较。鉴于 [14] 中解释的使用直线初始化基于ESDF的轨迹生成器时成功率较低，我们采用无碰撞初始化。比较结果如表II所示。
为了清晰起见，具有和不具有无碰撞初始化的基于ESDF的方法分别缩写为 $EI$ 和 $ENI$。此比较表明，所提出的EGO算法实现了与具有无碰撞初始化的基于ESDF的方法相当的成功率。然而，EGO产生的轨迹能量（加加速度积分）略高。这是因为EGO的控制点包含多个 $\{\mathbf{p},\mathbf{v}\}$ 对，产生的轨迹变形力比EI更强，如第IV-A2节所述。另一方面，更强的力加速了收敛过程，导致更短的优化时间。ENI的一些统计数据（以灰色显示）可能不太令人信服，因为ENI测试只能在较少的挑战案例中成功，在这些案例中，与EI和EGO相比，生成的轨迹自然更平滑，能量成本更低，速度更低。值得注意的是，虽然对于 $9m$ 的轨迹，ESDF更新大小减少到 $10\times 4\times 2m^3$，分辨率为 $0.1m$，但ESDF更新仍然占据了大部分计算时间。

# D. 多种规划器比较
我们将所提出的规划器与两种最先进的方法 Fast-Planner [14] 和 EWOK [2] 进行比较，这两种方法利用ESDF来评估障碍物距离和梯度。每个规划器在不同的障碍物密度下从相同的起点到终点运行十次。平均性能统计数据和ESDF计算时间如表III和图7所示。三种方法在0.5个障碍物/$m^2$的地图上生成的轨迹如图8所示。

从表3可以得出结论：与快速规划器相比，所提方法的飞行时间更短、轨迹长度更短，但能耗更高。
这主要是由文献[14]提出的前端动力学路径搜索方法导致的。
由于目标函数中包含指数项，EWOK在密集环境下会生成扭曲的轨迹，进而造成优化过程收敛不稳定。
此外，我们还发现，所提方法省去了环境有向距离场的更新步骤，因此节省了大量计算时间。


$^{2}$ https://www.intelrealsense.com/depth-camera-d435/
ZHOU et al.: EGO-PLANNER: AN ESDF-FREE GRADIENT-BASED LOCAL PLANNER FOR QUADROTORS
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/3c952de0078f759c831dadf505ff78a1e401afbceff8310cf9958c87ccd21a86.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/25c0ea729751204c548b4839df1b7544795b075ab0cd20aa80d33169e778c693.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/e313b3dd463c877cbee01705ec7e0bba0995f322c22436e716675605093f886a.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/92244f9d43b6e18e07cfdbd16d3e9d0b9f17019a0441d9776b6526f7a621760e.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/4bd50d736959c93437f4652a5674b90893f2d864db363b4c7d3bb9f4f62524d6.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/a50c9ff7bb0963720e44ee290b0c1b64fc4d3503d9ce06a31201ec8d2c10cb84.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/b801ef618224bcd4cafc1f4bc21e7799978e4ebbefb894ffc0ce9ffe80683e13.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/6403494b8b0b82867e5c0479eb7a51df4ee99c48c3c66d30a269384f5ef1f367.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/70a010ebb088bfc2a3fe3527d1043c14d6cf4d679834b436efe2db728214f681.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/00d55c3984140e800c9fa50b7278b54fe71860228b6ed2e32adfcfcb9d99f4d2.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/e402213dffa7136db27a7e0e28b1950c641c3fc0744df39243a692aeffdc27b2.jpg)


图 6：短时间内局部轨迹规划的可视化及速度分布。

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/44926f809432287f60e3e3c4acc8cb8e62e562c3bd412eec7c5c52e2710df011.jpg)


图 7：所提出的EGO-Planner与两种SOTA规划器在默认参数下的比较。


表 III：规划器比较

<table><tr><td>规划器</td><td>t(s)</td><td>长度</td><td>能量</td><td>tESDF(ms)</td><td>tplan(ms)</td></tr><tr><td>EWOK</td><td>31.00</td><td>59.05</td><td>246.12</td><td>6.43</td><td>1.39</td></tr><tr><td>Fast-Planner</td><td>30.76</td><td>45.18</td><td>135.21</td><td>4.01</td><td>3.29</td></tr><tr><td>EGO-Planner</td><td>24.38</td><td>42.24</td><td>196.64</td><td>/</td><td>0.81</td></tr></table>


# E. 真实世界实验
我们在视野有限的复杂未知环境中进行了几次实验。一个实验是按预先给定的航点飞行。在这个实验中，无人机从一个小办公室房间出发，穿过门，在一个大的杂乱房间里飞行，然后返回办公室，如图10a和图11所示。室内实验的最窄通道小于一米，如图6所示。相比之下，无人机在如此杂乱的环境中达到了 $3.56m/s$ 的速度。
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/f9e13e8d7451aa5c5ff9c2610b11e4c78064c6af2a3d5ae87e450e2639bfdaaa.jpg)


图 8：仿真中的轨迹可视化。

另一个室内实验是追逐飞行过程中任意突然给出的目标，如图10c所示。在这个测试中，有限的FOV带来了更大的挑战，即一旦接收到新目标或检测到碰撞威胁，必须立即生成可行的轨迹。因此，该实验验证了所提出的规划器能够在可行性的前提下进行激进飞行。
在户外实验中，无人机飞过一片巨大的树木和低矮灌木丛林，如图10b和图9所示。虽然无人机周围的狂野气流导致树枝和树叶摆动，使得地图不太可靠，但无人机仍然达到了 $3m / s$ 以上的速度。因此，所提出的规划器可以应对实验和野外环境。我们建议读者观看视频<sup>3</sup>以获取更多信息。
# VII. 结论与未来工作
在本文中，我们研究了ESDF对于基于梯度的轨迹规划的必要性，并提出了一种无ESDF的局部规划器。它实现了与一些最先进的基于ESDF的规划器相当的性能，但将计算时间减少了一个数量级以上。基准比较和真实世界实验验证了其鲁棒性和高效性。
7
3https://youtu.be/UKoagW7t7Dk
IEEE 机器人与自动化快报。预印本。2020年10月接受
![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/14fe3aa9db2e651a3e840933c300fca0ad0cff97c43b235b74022741722515a7.jpg)


图 9：森林中户外实验的轨迹。

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/ee132d1eb11220a5cba740ddbc551e9337d4167980beb7e026ffe6472aacef96.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/ffa0c98dfebb46577b172d21233218b5af3ff7f8d1fab9ed0e1b01d2574afac8.jpg)

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/f6dd9be5136ea0db4ed3a0cd2cd41139beb84586aa4ee3ab79ddd72780e8ef39.jpg)


图 10：真实世界实验。a) 室内测试。b) 户外测试。c) 室内飞行的合成快照。

![image](https://cdn-mineru.openxlab.org.cn/result/2025-12-15/3ebfa7d2-2319-47e2-809b-b0e447754561/cb1377577ccc0e4f0e8450b11c13965c56de2e0b2a6fb3cb63730b867b2951fc.jpg)


图 11：室内实验的轨迹

所提出的方法仍然存在一些缺陷，即由 $\mathrm{A}^*$ 搜索引入的局部极小值和由统一时间重分配引入的保守轨迹。因此，我们将致力于执行拓扑规划以逃离局部极小值，并重新表述问题以生成近乎最优的轨迹。该规划器专为静态环境设计，无需任何修改即可应对缓慢移动的障碍物（低于 $0.5\mathrm{m / s}$）。未来我们将致力于通过移动物体检测和拓扑规划来实现动态环境导航。
# 参考文献


[1] L. Quan, L. Han, B. Zhou, S. Shen, and F. Gao, "Survey of uav motion planning," IET Cyber-systems and Robotics, vol. 2, no. 1, pp. 14-21, 2020.




[2] V. Usenko, L. von Stumberg, A. Pangercic, and D. Cremers, "Real-time trajectory replanning for mavs using uniform b-splines and a 3d circular buffer," in Proc. of the IEEE/RSJ Intl. Conf. on Intell. Robots and Syst.(IROS). IEEE, 2017, pp. 215-222.




[3] L. Han, F. Gao, B. Zhou, and S. Shen, "Fiesta: Fast incremental euclidean distance fields for online motion planning of aerial robots," in Proc. of the IEEE/RSJ Intl. Conf. on Intell. Robots and Syst.(IROS). IEEE, 2019, pp. 4423-4430.




[4] P. F. Felzenszwalb and D. P. Huttenlocher, “Distance transforms of sampled functions,” Theory of Computing, vol. 8, no. 1, pp. 415–428, 2012.




[5] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, "Chomp: Gradient optimization techniques for efficient motion planning," in Proc. of the IEEE Intl. Conf. on Robot. and Autom. (ICRA), May 2009, pp. 489-494.




[6] M. Kalakrishnan, S. Chitta, E. Theodorou, P. Pastor, and S. Schaal, "Stomp: Stochastic trajectory optimization for motion planning," in Proc. of the IEEE Intl. Conf. on Robot. and Autom. (ICRA). IEEE, 2011, pp. 4569-4574.




[7] H. Oleynikova, M. Burri, Z. Taylor, J. Nieto, R. Siegwart, and E. Galceran, "Continuous-time trajectory optimization for online uav replanning," in Proc. of the IEEE/RSJ Intl. Conf. on Intell. Robots and Syst.(IROS), Daejeon, Korea, Oct. 2016, pp. 5332-5339.




[8] F. Gao, Y. Lin, and S. Shen, "Gradient-based online safe trajectory generation for quadrotor flight in complex environments," in Proc. of the IEEE/RSJ Intl. Conf. on Intell. Robots and Syst.(IROS). IEEE, 2017, pp. 3681-3688.




[9] W. Ding, W. Gao, K. Wang, and S. Shen, "An efficient b-spline-based kinodynamic replanning framework for quadrotors," IEEE Transactions on Robotics, vol. 35, no. 6, pp. 1287-1306, 2019.




[10] B. Zhou, F. Gao, L. Wang, C. Liu, and S. Shen, “Robust and efficient quadrotor trajectory generation for fast autonomous flight,” IEEE Robotics and Automation Letters, vol. 4, no. 4, pp. 3529–3536, 2019.




[11] B. Zhou, J. Pan, F. Gao, and S. Shen, "Raptor: Robust and perception-aware trajectory replanning for quadrotor fast flight," arXiv preprint arXiv:2007.03465, 2020.




[12] B. Curless and M. Levoy, "A volumetric method for building complex models from range images," in Proceedings of the 23rd annual conference on Computer graphics and interactive techniques, 1996, pp. 303-312.




[13] H. Oleynikova, Z. Taylor, M. Fehr, R. Siegwart, and J. Nieto, "Voxelbox: Incremental 3d euclidean signed distance fields for on-board mav planning," in Proc. of the IEEE/RSJ Intl. Conf. on Intell. Robots and Syst.(IROS), 2017.




[14] B. Zhou, F. Gao, L. Wang, C. Liu, and S. Shen, “Robust and efficient quadrotor trajectory generation for fast autonomous flight,” IEEE Robotics and Automation Letters, vol. 4, no. 4, pp. 3529–3536, 2019.




[15] D. Mellinger and V. Kumar, "Minimum snap trajectory generation and control for quadrotors," in Proc. of the IEEE Intl. Conf. on Robot. and Autom. (ICRA), Shanghai, China, May 2011, pp. 2520-2525.




[16] J. Barzilai and J. M. Borwein, “Two-point step size gradient methods,” Ima Journal of Numerical Analysis, vol. 8, no. 1, pp. 141–148, 1988.




[17] R. D. T. STEIHA, "Truncatednewton algorithmsforlarge-scale optimization," Math. Programming, vol. 26, pp. 190-212, 1983.




[18] D. C. Liu and J. Nocedal, "On the limited memory bfgs method for large scale optimization," Mathematical programming, vol. 45, no. 1-3, pp. 503-528, 1989.




[19] F. Gao, L. Wang, B. Zhou, X. Zhou, J. Pan, and S. Shen, "Teach-repeat-replan: A complete and robust system for aggressive flight in complex environments," IEEE Transactions on Robotics, 2020.