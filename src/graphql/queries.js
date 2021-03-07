/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getCalendar = /* GraphQL */ `
  query GetCalendar($owner: String!, $calendarId: String!) {
    getCalendar(owner: $owner, calendarId: $calendarId) {
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
export const listCalendar = /* GraphQL */ `
  query ListCalendar(
    $owner: String
    $calendarId: ModelStringKeyConditionInput
    $filter: ModelYoteiasobiCalendarFilterInput
    $limit: Int
    $nextToken: String
    $sortDirection: ModelSortDirection
  ) {
    listCalendar(
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
        title
        image
        description
        address
        tel
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
