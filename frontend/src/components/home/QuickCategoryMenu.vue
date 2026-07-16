<script setup>
import{computed}from'vue';import{filterIconFor}from'../../utils/mapAssets'
const props=defineProps({modelValue:{type:String,default:'전체'}}),emit=defineEmits(['update:modelValue'])
const categories=[['전체','전체'],['다가오는 축제','축제'],['무료 축제','축제'],['공연','공연'],['전시','전시'],['전통','전통'],['야외 행사','야외 행사']]
const active=computed({get:()=>props.modelValue,set:v=>emit('update:modelValue',v)})
</script>
<template><section class="container quick-wrap section-card"><div class="quick-scroll"><button v-for="[label,type] in categories" :key="label" :class="{active:active===label}" @click="active=label"><img :src="filterIconFor(type)" alt=""><span>{{ label }}</span></button></div></section></template>
<style scoped>
.quick-wrap{padding:0 18px;border-radius:18px}.quick-scroll{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));overflow-x:auto}.quick-scroll button{min-height:68px;display:flex;align-items:center;justify-content:center;gap:10px;border:0;background:transparent;font-size:14px;font-weight:800;white-space:nowrap}.quick-scroll button.active{color:var(--color-primary-dark)}.quick-scroll img{width:34px;height:34px;object-fit:contain}@media(max-width:980px){.quick-scroll{grid-template-columns:repeat(7,130px)}}@media(max-width:560px){.quick-wrap{padding:0 8px}.quick-scroll{grid-template-columns:repeat(7,112px)}.quick-scroll button{font-size:12px}}
</style>
