/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createCalendar = /* GraphQL */ `
  mutation CreateCalendar(
    $input: CreateYoteiasobiCalendarInput!
    $condition: ModelYoteiasobiCalendarConditionInput
  ) {
    createCalendar(input: $input, condition: $condition) {
      owner
      calendarId
      title
      image
      description
      address
      tel
      createdAt
      updatedAt
    }
  }
`;
export const deleteCalendar = /* GraphQL */ `
  mutation DeleteCalendar(
    $input: DeleteYoteiasobiCalendarInput!
    $condition: ModelYoteiasobiCalendarConditionInput
  ) {
    deleteCalendar(input: $input, condition: $condition) {
      owner
      calendarId
      title
      image
      description
      address
      tel
      createdAt
      updatedAt
    }
  }
`;
export const createCalendar2 = /* GraphQL */ `
  mutation CreateCalendar2(
    $input: CreateYoteiasobiCalendar2Input!
    $condition: ModelYoteiasobiCalendar2ConditionInput
  ) {
    createCalendar2(input: $input, condition: $condition) {
      calendarId
      title
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const deleteCalendar2 = /* GraphQL */ `
  mutation DeleteCalendar2(
    $input: DeleteYoteiasobiCalendar2Input!
    $condition: ModelYoteiasobiCalendar2ConditionInput
  ) {
    deleteCalendar2(input: $input, condition: $condition) {
      calendarId
      title
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const createPrivateNote = /* GraphQL */ `
  mutation CreatePrivateNote(
    $input: CreatePrivateNoteInput!
    $condition: ModelPrivateNoteConditionInput
  ) {
    createPrivateNote(input: $input, condition: $condition) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
export const updatePrivateNote = /* GraphQL */ `
  mutation UpdatePrivateNote(
    $input: UpdatePrivateNoteInput!
    $condition: ModelPrivateNoteConditionInput
  ) {
    updatePrivateNote(input: $input, condition: $condition) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
export const deletePrivateNote = /* GraphQL */ `
  mutation DeletePrivateNote(
    $input: DeletePrivateNoteInput!
    $condition: ModelPrivateNoteConditionInput
  ) {
    deletePrivateNote(input: $input, condition: $condition) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
