/*
THIS IS A GENERATED/BUNDLED FILE BY ROLLUP
if you want to view the source visit the plugins github repository
*/

'use strict';

var obsidian = require('obsidian');

/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

function __awaiter(thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
}

class RegexPipeline extends obsidian.Plugin {
    constructor() {
        super(...arguments);
        this.pathToRulesets = this.app.vault.configDir + "/regex-rulesets";
        this.indexFile = "/index.txt";
    }
    log(message, ...optionalParams) {
        // comment this to disable logging
        console.log("[regex-pipeline] " + message);
    }
    onload() {
        return __awaiter(this, void 0, void 0, function* () {
            this.log('loading');
            this.addSettingTab(new ORPSettings(this.app, this));
            this.configs = yield this.loadData();
            if (this.configs == null)
                this.configs = new SavedConfigs(3, 3, false);
            if (this.configs.rulesInVault)
                this.pathToRulesets = "/regex-rulesets";
            this.menu = new ApplyRuleSetMenu(this.app, this);
            this.menu.contentEl.className = "rulesets-menu-content";
            this.menu.titleEl.className = "rulesets-menu-title";
            this.addRibbonIcon('dice', 'Regex Rulesets', () => {
                this.menu.open();
            });
            this.addCommand({
                id: 'apply-ruleset',
                name: 'Apply Ruleset',
                // callback: () => {
                // 	this.log('Simple Callback');
                // },
                checkCallback: (checking) => {
                    let leaf = this.app.workspace.activeLeaf;
                    if (leaf) {
                        if (!checking) {
                            this.menu.open();
                        }
                        return true;
                    }
                    return false;
                }
            });
            this.reloadRulesets();
            this.log("Rulesets: " + this.pathToRulesets);
            this.log("Index: " + this.pathToRulesets + this.indexFile);
        });
    }
    onunload() {
        this.log('unloading');
        if (this.rightClickEventRef != null)
            this.app.workspace.offref(this.rightClickEventRef);
    }
    reloadRulesets() {
        return __awaiter(this, void 0, void 0, function* () {
            if (!(yield this.app.vault.adapter.exists(this.pathToRulesets)))
                yield this.app.vault.createFolder(this.pathToRulesets);
            if (!(yield this.app.vault.adapter.exists(this.pathToRulesets + this.indexFile)))
                yield this.app.vault.adapter.write(this.pathToRulesets + this.indexFile, "").catch((r) => {
                    new obsidian.Notice("Failed to write to index file: " + r);
                });
            let p = this.app.vault.adapter.read(this.pathToRulesets + this.indexFile);
            p.then(s => {
                this.rules = s.split(/\r\n|\r|\n/);
                this.rules = this.rules.filter((v) => v.length > 0);
                this.log(this.rules);
                this.updateRightclickMenu();
                this.updateQuickCommands();
            });
        });
    }
    updateQuickCommands() {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.configs.quickCommands <= 0)
                return;
            if (this.quickCommands == null)
                this.quickCommands = new Array();
            let expectedCommands = Math.min(this.configs.quickCommands, this.rules.length);
            this.log(`setting up ${expectedCommands} commands...`);
            for (let i = 0; i < expectedCommands; i++) {
                let r = this.rules[i];
                let c = this.addCommand({
                    id: `ruleset: ${r}`,
                    name: r,
                    editorCheckCallback: (checking) => {
                        if (checking)
                            return this.rules.contains(r);
                        this.applyRuleset(this.pathToRulesets + "/" + r);
                    },
                });
                this.log(`pusing ${r} command...`);
                this.quickCommands.push(c);
                this.log(this.quickCommands);
            }
        });
    }
    updateRightclickMenu() {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.rightClickEventRef != null)
                this.app.workspace.offref(this.rightClickEventRef);
            this.rightClickEventRef = this.app.workspace.on("editor-menu", (menu) => {
                for (let i = 0; i < Math.min(this.configs.quickRules, this.rules.length); i++) {
                    let rPath = this.pathToRulesets + "/" + this.rules[i];
                    menu.addItem((item) => {
                        item.setTitle("Regex Pipeline: " + this.rules[i])
                            .onClick(() => {
                            this.applyRuleset(rPath);
                        });
                    });
                }
            });
            this.registerEvent(this.rightClickEventRef);
        });
    }
    appendRulesetsToIndex(name) {
        return __awaiter(this, void 0, void 0, function* () {
            var result = true;
            this.rules.push(name);
            var newIndexValue = "";
            this.rules.forEach((v, i, all) => {
                newIndexValue += v + "\n";
            });
            yield this.app.vault.adapter.write(this.pathToRulesets + this.indexFile, newIndexValue).catch((r) => {
                new obsidian.Notice("Failed to write to index file: " + r);
                result = false;
            });
            return result;
        });
    }
    createRuleset(name, content) {
        return __awaiter(this, void 0, void 0, function* () {
            this.log("createRuleset: " + name);
            var path = this.pathToRulesets + "/" + name;
            if (yield this.app.vault.adapter.exists(path)) {
                this.log("file existed: " + path);
                return false;
            }
            yield this.app.vault.adapter.write(path, content).catch((r) => {
                new obsidian.Notice("Failed to write the ruleset file: " + r);
            });
            yield this.appendRulesetsToIndex(name);
            return true;
        });
    }
    applyRuleset(ruleset) {
        return __awaiter(this, void 0, void 0, function* () {
            if (!(yield this.app.vault.adapter.exists(ruleset))) {
                new obsidian.Notice(ruleset + " not found!");
                return;
            }
            let ruleParser = /^"(.+?)"([a-z]*?)(?:\r\n|\r|\n)?->(?:\r\n|\r|\n)?"(.*?)"([a-z]*?)(?:\r\n|\r|\n)?$/gmus;
            let ruleText = yield this.app.vault.adapter.read(ruleset);
            let activeMarkdownView = this.app.workspace.getActiveViewOfType(obsidian.MarkdownView);
            if (activeMarkdownView == null) {
                new obsidian.Notice("No active Markdown file!");
                return;
            }
            let subject;
            let selectionMode;
            if (activeMarkdownView.editor.somethingSelected()) {
                subject = activeMarkdownView.editor.getSelection();
                selectionMode = true;
            }
            else {
                subject = activeMarkdownView.editor.getValue();
            }
            let pos = activeMarkdownView.editor.getScrollInfo();
            this.log(pos.top);
            let count = 0;
            let ruleMatches;
            while (ruleMatches = ruleParser.exec(ruleText)) {
                if (ruleMatches == null)
                    break;
                this.log("\n" + ruleMatches[1] + "\n↓↓↓↓↓\n" + ruleMatches[3]);
                let matchRule = ruleMatches[2].length == 0 ? new RegExp(ruleMatches[1], 'gm') : new RegExp(ruleMatches[1], ruleMatches[2]);
                if (ruleMatches[4] == 'x')
                    subject = subject.replace(matchRule, '');
                else
                    subject = subject.replace(matchRule, ruleMatches[3]);
                count++;
            }
            if (selectionMode)
                activeMarkdownView.editor.replaceSelection(subject);
            else
                activeMarkdownView.editor.setValue(subject);
            activeMarkdownView.requestSave();
            activeMarkdownView.editor.scrollTo(0, pos.top);
            new obsidian.Notice("Executed ruleset '" + ruleset + "' which contains " + count + " regex replacements!");
        });
    }
}
class SavedConfigs {
    constructor(quickRules, quickCommands, rulesInVault) {
        this.quickRules = quickRules;
        this.rulesInVault = rulesInVault;
        this.quickCommands = quickCommands;
    }
}
class ORPSettings extends obsidian.PluginSettingTab {
    constructor(app, plugin) {
        super(app, plugin);
    }
    display() {
        this.containerEl.empty();
        new obsidian.Setting(this.containerEl)
            .setName("Quick Rules")
            .setDesc("The first N rulesets in your index file will be available in right click menu and as commands.")
            .addSlider(c => {
            c.setValue(this.plugin.configs.quickRules);
            c.setLimits(0, 10, 1);
            c.setDynamicTooltip();
            c.showTooltip();
            c.onChange((v) => {
                if (v != this.plugin.configs.quickRules)
                    this.plugin.quickRulesChanged = true;
                this.plugin.configs.quickRules = v;
            });
        });
        new obsidian.Setting(this.containerEl)
            .setName("Quick Rule Commands")
            .setDesc("The first N rulesets in your index file will be available as Obsidian commands. If decreasing, the existing commands will not be removed until next reload (You can also manually re-enabled the plugin).")
            .addSlider(c => {
            c.setValue(this.plugin.configs.quickCommands);
            c.setLimits(0, 10, 1);
            c.setDynamicTooltip();
            c.showTooltip();
            c.onChange((v) => {
                this.plugin.configs.quickCommands = v;
                this.plugin.updateQuickCommands();
            });
        });
        new obsidian.Setting(this.containerEl)
            .setName("Save Rules In Vault")
            .setDesc("Reads rulesets from \".obsidian/regex-rulesets\" when off, \"./regex-ruleset\" when on (useful if you are user of ObsidianSync). ")
            .addToggle(c => {
            c.setValue(this.plugin.configs.rulesInVault);
            c.onChange(v => {
                this.plugin.configs.rulesInVault = v;
                if (v)
                    this.plugin.pathToRulesets = "/regex-rulesets";
                else
                    this.plugin.pathToRulesets = this.app.vault.configDir + "/regex-rulesets";
            });
        });
    }
    hide() {
        this.plugin.reloadRulesets();
        this.plugin.saveData(this.plugin.configs);
    }
}
class ApplyRuleSetMenu extends obsidian.Modal {
    constructor(app, plugin) {
        super(app);
        this.plugin = plugin;
        this.modalEl.style.setProperty("width", "60vw");
        this.modalEl.style.setProperty("max-height", "60vh");
        this.modalEl.style.setProperty("padding", "2rem");
        this.titleEl.createEl("h1", null, el => {
            el.innerHTML = this.plugin.pathToRulesets + "/...";
            el.style.setProperty("display", "inline-block");
            el.style.setProperty("width", "92%");
            el.style.setProperty("max-width", "480px");
            el.style.setProperty("margin", "12 0 8");
        });
        this.titleEl.createEl("h1", null, el => { el.style.setProperty("flex-grow", "1"); });
        var reloadButton = new obsidian.ButtonComponent(this.titleEl)
            .setButtonText("RELOAD")
            .onClick((evt) => __awaiter(this, void 0, void 0, function* () {
            yield this.plugin.reloadRulesets();
            this.onClose();
            this.onOpen();
        }));
        reloadButton.buttonEl.style.setProperty("display", "inline-block");
        reloadButton.buttonEl.style.setProperty("bottom", "8px");
        reloadButton.buttonEl.style.setProperty("margin", "auto");
    }
    onOpen() {
        for (let i = 0; i < this.plugin.rules.length; i++) {
            // new Setting(contentEl)
            // 	.setName(this.plugin.rules[i])
            // 	.addButton(btn => btn.onClick(async () => {
            // 		this.plugin.applyRuleset(this.plugin.pathToRulesets + "/" + this.plugin.rules[i])
            // 		this.close();
            // 	}).setButtonText("Apply"));
            var ruleset = new obsidian.ButtonComponent(this.contentEl)
                .setButtonText(this.plugin.rules[i])
                .onClick((evt) => __awaiter(this, void 0, void 0, function* () {
                this.plugin.applyRuleset(this.plugin.pathToRulesets + "/" + this.plugin.rules[i]);
                this.close();
            }));
            ruleset.buttonEl.className = "apply-ruleset-button";
        }
        this.titleEl.getElementsByTagName("h1")[0].innerHTML = this.plugin.pathToRulesets + "/...";
        var addButton = new obsidian.ButtonComponent(this.contentEl)
            .setButtonText("+")
            .onClick((evt) => __awaiter(this, void 0, void 0, function* () {
            new NewRulesetPanel(this.app, this.plugin).open();
        }));
        addButton.buttonEl.className = "add-ruleset-button";
        addButton.buttonEl.style.setProperty("width", "3.3em");
    }
    onClose() {
        let { contentEl } = this;
        contentEl.empty();
    }
}
class NewRulesetPanel extends obsidian.Modal {
    constructor(app, plugin) {
        super(app);
        this.plugin = plugin;
        this.contentEl.className = "ruleset-creation-content";
    }
    onOpen() {
        var nameHint = this.contentEl.createEl("h4");
        nameHint.innerHTML = "Name";
        this.contentEl.append(nameHint);
        var nameInput = this.contentEl.createEl("textarea");
        nameInput.setAttr("rows", "1");
        nameInput.addEventListener('keydown', (e) => {
            if (e.key === "Enter")
                e.preventDefault();
        });
        this.contentEl.append(nameInput);
        var contentHint = this.contentEl.createEl("h4");
        contentHint.innerHTML = "Content";
        this.contentEl.append(contentHint);
        var contentInput = this.contentEl.createEl("textarea");
        contentInput.style.setProperty("height", "300px");
        this.contentEl.append(contentInput);
        new obsidian.ButtonComponent(this.contentEl)
            .setButtonText("Save")
            .onClick((evt) => __awaiter(this, void 0, void 0, function* () {
            if (!(yield this.plugin.createRuleset(nameInput.value, contentInput.value))) {
                new obsidian.Notice("Failed to create the ruleset! Please check if the file already exist.");
                return;
            }
            this.plugin.menu.onClose();
            this.plugin.menu.onOpen();
            this.close();
        }));
    }
    onClose() {
        let { contentEl } = this;
        contentEl.empty();
    }
}

module.exports = RegexPipeline;


/* nosourcemap */