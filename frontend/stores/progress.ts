import { defineStore } from 'pinia'
import type { RecurringIssue } from '~/types/protocol'

export const useProgressStore = defineStore('progress', () => {
  const recurringIssues = ref<RecurringIssue[]>([])
  const suggestedFocus = ref<string[]>([])

  function update(issues: RecurringIssue[], focus: string[]) {
    recurringIssues.value = issues; suggestedFocus.value = focus
  }
  function reset() { recurringIssues.value = []; suggestedFocus.value = [] }

  return { recurringIssues, suggestedFocus, update, reset }
})
