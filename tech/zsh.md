# Zsh + Oh My Zsh + Powerlevel10k 配置指南

## 1. 先安装依赖和 zsh
打开终端，复制执行这一行：
```bash
sudo apt update && sudo apt install -y zsh git curl wget fontconfig
```

## 2. 安装 Oh My Zsh
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
执行过程中会问你：**Do you want to change your default shell to zsh?**  
输入 `y` 并回车。

> 如果中途卡住：按 `Ctrl+C` 退出，重新执行一遍即可。

## 3. 安装 Powerlevel10k 主题
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

## 4. 替换配置文件（关键）
```bash
sed -i 's/^ZSH_THEME=".*"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc
```

## 5. 重启 zsh 开始配置 p10k
```bash
exec zsh
```
会自动弹出 p10k 配置向导，按照你喜欢的风格选择即可：
- 字体是否显示正常？选 `y`
- 风格推荐：**3 (Rainbow)** 最好看
- 其他一路默认回车就行

## 6. 以后想重新配置 p10k
```bash
p10k configure
```
## 7. 安装实用插件

```bash
# 语法高亮
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 历史命令自动补全建议
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

## 8. 启用插件（修改 .zshrc）
编辑配置文件：
```bash
nano ~/.zshrc
```

找到 `plugins=` 这一行，替换为：
```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```