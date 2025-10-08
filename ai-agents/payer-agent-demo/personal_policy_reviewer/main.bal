import ballerina/ai;
import ballerina/http;

listener ai:Listener policyReviewerListener = new (listenOn = check http:getDefaultListener());

service /policyReviewer on policyReviewerListener {
    resource function post chat(@http:Payload ai:ChatReqMessage request) returns ai:ChatRespMessage|error {
        string stringResult = check _policyReviewerAgent.run(request.message, request.sessionId);
        return {message: stringResult};
    }
}
