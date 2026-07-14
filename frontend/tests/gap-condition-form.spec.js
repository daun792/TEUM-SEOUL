import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import GapConditionForm from '../src/components/course/GapConditionForm.vue'


describe('GapConditionForm', () => {
  it('rejects time outside 30 to 180 minutes', async () => {
    const wrapper = mount(GapConditionForm, {
      props: { performance: { id: 1, name: '테스트 공연' } },
    })
    await wrapper.find('[name="availableMinutes"]').setValue('20')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toBeUndefined()
    expect(wrapper.text()).toContain('30분에서 180분 사이')
  })

  it('emits normalized recommendation conditions', async () => {
    const wrapper = mount(GapConditionForm, {
      props: { performance: { id: 9, name: '테스트 공연' } },
    })
    await wrapper.find('input[name="phase"][value="after"]').setValue()
    await wrapper.find('[name="availableMinutes"]').setValue('120')
    await wrapper.find('[name="preferredCategory"]').setValue('문화시설')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')[0][0]).toEqual({
      performance_id: 9,
      phase: 'after',
      available_minutes: 120,
      preferred_category: '문화시설',
    })
  })
})
