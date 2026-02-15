<template>
  <li class="tree-node">
    <div class="tree-node-content" @click="$emit('toggle', node)">
      <span class="tree-icon">{{ node.expanded ? '📁' : '📂' }}</span>
      <span class="tree-label">{{ node.name }}</span>
      <div class="tree-node-actions">
        <button class="tree-action-btn" @click.stop="$emit('create-folder', node)">📁</button>
        <button class="tree-action-btn" @click.stop="$emit('upload-file', node)">⬆️</button>
        <button class="tree-action-btn" @click.stop="$emit('delete', node)">🗑️</button>
      </div>
    </div>
    <ul v-if="node.expanded && node.children.length > 0" class="tree-children">
      <tree-node
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        @toggle="$emit('toggle', $event)"
        @create-folder="$emit('create-folder', $event)"
        @upload-file="$emit('upload-file', $event)"
        @delete="$emit('delete', $event)"
      />
    </ul>
  </li>
</template>

<script setup lang="ts">
defineProps({
  node: {
    type: Object,
    required: true
  }
})

defineEmits(['toggle', 'create-folder', 'upload-file', 'delete'])
</script>

<style scoped>
.tree-node {
  margin-bottom: 5px;
}

.tree-node-content {
  display: flex;
  align-items: center;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}

.tree-node-content:hover {
  background-color: #f8f9fa;
}

.tree-icon {
  margin-right: 10px;
  font-size: 16px;
  flex-shrink: 0;
}

.tree-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 10px;
}

.tree-node-actions {
  display: flex;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.2s;
  flex-shrink: 0;
  min-width: 60px;
  justify-content: flex-end;
}

.tree-node-content:hover .tree-node-actions {
  opacity: 1;
}

.tree-action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 2px;
}

.tree-children {
  list-style: none;
  padding-left: 25px;
  margin-top: 5px;
}
</style>