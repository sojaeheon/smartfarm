<template>
  <div class="modal-overlay" @click="$emit('closeModal')">
    <div class="modal" @click.stop>
      <ul>
        <li v-for="(list, index) in lists" :key="index" @click="$emit('selectSession', list.session_id)"
         class="modal-item">
          {{ list.question }}
          <button class="del_button" @click.stop="$emit('deleteItem', index)"></button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    lists: {
      type: Array,
      required: true
    }
  }
};
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  /* 반투명 배경 */
  display: flex;
  justify-content: flex-end;
  /* 오른쪽 정렬 */
  align-items: flex-start;
  /* 위쪽 정렬 */
  z-index: 3;
}

.modal {
  margin: 20px;
  /* 모달과 화면 가장자리 간의 여백 */
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  /* 최소 너비 */
  cursor: pointer;
}

.modal-item {
  display: block;
  width: 100%; /* 도형의 크기에 맞게 조정 */
  white-space: nowrap; /* 텍스트를 한 줄로 표시 */
  overflow: hidden; /* 넘치는 텍스트 숨기기 */
  text-overflow: ellipsis; /* 넘치는 부분을 줄임표(...)로 표시 */
}

.del_button {
  background-image: url('@/assets/closebutton.svg');
  width: 20px;
  height: 20px;
  position: absolute;
  right: 3vw; 

}
</style>
