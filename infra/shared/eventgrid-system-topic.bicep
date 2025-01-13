param systemTopicName string
param topicType string
param location string
param sourceResourceId string

resource systemTopic 'Microsoft.EventGrid/systemTopics@2021-06-01-preview' = {
  name: systemTopicName
  location: location
  properties: {
    topicType: topicType
    source: sourceResourceId
  }
}

output name string = systemTopic.name
output id string = systemTopic.id
