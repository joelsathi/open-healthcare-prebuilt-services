import ballerina/ai;
import ballerina/http;

listener ai:Listener medicalPolicyReviewerListener = new (listenOn = check http:getDefaultListener());

service /medicalPolicyReviewer on medicalPolicyReviewerListener {
    resource function post chat(@http:Payload ai:ChatReqMessage request) returns ai:ChatRespMessage|error {
        string stringResult = check _medicalPolicyReviewerAgent.run(request.message, request.sessionId);
        return {message: stringResult};
    }
}
