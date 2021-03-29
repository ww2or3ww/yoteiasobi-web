/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onCreateCalendarAll = /* GraphQL */ `
  subscription OnCreateCalendarAll {
    onCreateCalendarAll {
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
export const onCreateCalendarBy = /* GraphQL */ `
  subscription OnCreateCalendarBy($owner: String!) {
    onCreateCalendarBy(owner: $owner) {
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
export const onCreateUserCalendarAll = /* GraphQL */ `
  subscription OnCreateUserCalendarAll {
    onCreateUserCalendarAll {
      owner
      calendarId
      creator
      createdAt
      updatedAt
    }
  }
`;
export const onCreateUserCalendarBy = /* GraphQL */ `
  subscription OnCreateUserCalendarBy($owner: String!) {
    onCreateUserCalendarBy(owner: $owner) {
      owner
      calendarId
      creator
      createdAt
      updatedAt
    }
  }
`;
export const onCreatePrivateNote = /* GraphQL */ `
  subscription OnCreatePrivateNote($owner: String!) {
    onCreatePrivateNote(owner: $owner) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
export const onUpdatePrivateNote = /* GraphQL */ `
  subscription OnUpdatePrivateNote($owner: String!) {
    onUpdatePrivateNote(owner: $owner) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
export const onDeletePrivateNote = /* GraphQL */ `
  subscription OnDeletePrivateNote($owner: String!) {
    onDeletePrivateNote(owner: $owner) {
      id
      content
      updatedAt
      createdAt
      owner
    }
  }
`;
