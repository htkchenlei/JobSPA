<template>
  <n-config-provider
    :theme-overrides="macaronThemeOverrides"
    :locale="zhCN"
    :date-locale="dateZhCN"
  >
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-message-provider :duration="2600" :max="3">
          <n-notification-provider :max="3">
            <router-view />
          </n-notification-provider>
        </n-message-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import {
  NConfigProvider,
  NDialogProvider,
  NLoadingBarProvider,
  NMessageProvider,
  NNotificationProvider,
  dateZhCN,
  zhCN
} from 'naive-ui'
import { macaronThemeOverrides } from './theme/naiveTheme'
</script>
