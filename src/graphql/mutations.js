/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const processYoteiasobi = /* GraphQL */ `
  mutation ProcessYoteiasobi($calendarId: String!, $content: String!) {
    processYoteiasobi(calendarId: $calendarId, content: $content) {
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
