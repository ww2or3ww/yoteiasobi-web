/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getCalendar = /* GraphQL */ `
  query GetCalendar($calendarId: String!) {
    getCalendar(calendarId: $calendarId) {
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
export const listCalendar = /* GraphQL */ `
  query ListCalendar(
    $calendarId: String
    $filter: ModelYoteiasobiCalendarFilterInput
    $limit: Int
    $nextToken: String
    $sortDirection: ModelSortDirection
  ) {
    listCalendar(
      calendarId: $calendarId
      filter: $filter
      limit: $limit
      nextToken: $nextToken
      sortDirection: $sortDirection
    ) {
      items {
        calendarId
        title
        image
        description
        createdAt
        updatedAt
        owner
      }
      nextToken
    }
  }
`;
export const getUserCalendar = /* GraphQL */ `
  query GetUserCalendar($owner: String!, $calendarId: String!) {
    getUserCalendar(owner: $owner, calendarId: $calendarId) {
      owner
      calendarId
      creator
      createdAt
      updatedAt
    }
  }
`;
export const listUserCalendar = /* GraphQL */ `
  query ListUserCalendar(
    $owner: String
    $calendarId: ModelStringKeyConditionInput
    $filter: ModelYoteiasobiUserCalendarFilterInput
    $limit: Int
    $nextToken: String
    $sortDirection: ModelSortDirection
  ) {
    listUserCalendar(
      owner: $owner
      calendarId: $calendarId
      filter: $filter
      limit: $limit
      nextToken: $nextToken
      sortDirection: $sortDirection
    ) {
      items {
        owner
        calendarId
        creator
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const getPrivateNote = /* GraphQL */ `
  query GetPrivateNote($id: ID!) {
    getPrivateNote(id: $id) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
export const listPrivateNotes = /* GraphQL */ `
  query ListPrivateNotes(
    $filter: ModelPrivateNoteFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listPrivateNotes(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        content
        updatedAt
        createdAt
        owner
      }
      nextToken
    }
  }
`;
