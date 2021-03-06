/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onCreateCalendarAll = /* GraphQL */ `
  subscription OnCreateCalendarAll {
    onCreateCalendarAll {
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
export const onCreateCalendarBy = /* GraphQL */ `
  subscription OnCreateCalendarBy($owner: String!) {
    onCreateCalendarBy(owner: $owner) {
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
export const onCreateCalendar2All = /* GraphQL */ `
  subscription OnCreateCalendar2All {
    onCreateCalendar2All {
      calendarId
      title
      description
      createdAt
      updatedAt
      owner
    }
  }
`;
export const onCreateCalendar2By = /* GraphQL */ `
  subscription OnCreateCalendar2By($owner: String!) {
    onCreateCalendar2By(owner: $owner) {
      calendarId
      title
      description
      createdAt
      updatedAt
      owner
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
