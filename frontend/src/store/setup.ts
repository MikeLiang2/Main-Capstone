// layout status and config

import { defineStore } from 'pinia';

let useSettingStore = defineStore('SettingStore', {
  state: () => {
    return {
      fold: false, // 用户控制菜单是展开还是收起
      refresh: false
    }
  }
})

export default useSettingStore;