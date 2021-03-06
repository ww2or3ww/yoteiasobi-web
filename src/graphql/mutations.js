/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const processYoteiasobi = /* GraphQL */ `
  mutation ProcessYoteiasobi($calendarId: String!, $content: String!) {
    processYoteiasobi(calendarId: $calendarId, content: $content) {
      calendarId
      title
      image
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const createCalendar = /* GraphQL */ `
  mutation CreateCalendar(
    $input: CreateYoteiasobiCalendarInput!
    $condition: ModelYoteiasobiCalendarConditionInput
  ) {
    createCalendar(input: $input, condition: $condition) {
      calendarId
      title
      image
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const updateCalendar = /* GraphQL */ `
  mutation UpdateCalendar(
    $input: UpdateYoteiasobiCalendarInput!
    $condition: ModelYoteiasobiCalendarConditionInput
  ) {
    updateCalendar(input: $input, condition: $condition) {
      calendarId
      title
      image
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const deleteCalendar = /* GraphQL */ `
  mutation DeleteCalendar(
    $input: DeleteYoteiasobiCalendarInput!
    $condition: ModelYoteiasobiCalendarConditionInput
  ) {
    deleteCalendar(input: $input, condition: $condition) {
      calendarId
      title
      image
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const createUserCalendar = /* GraphQL */ `
  mutation CreateUserCalendar(
    $input: CreateYoteiasobiUserCalendarInput!
    $condition: ModelYoteiasobiUserCalendarConditionInput
  ) {
    createUserCalendar(input: $input, condition: $condition) {
      owner
      calendarId
      creator
      createdAt
      updatedAt
    }
  }
`;
export const deleteUserCalendar = /* GraphQL */ `
  mutation DeleteUserCalendar(
    $input: DeleteYoteiasobiUserCalendarInput!
    $condition: ModelYoteiasobiUserCalendarConditionInput
  ) {
    deleteUserCalendar(input: $input, condition: $condition) {
      owner
      calendarId
      creator
      createdAt
      updatedAt
    }
  }
`;
