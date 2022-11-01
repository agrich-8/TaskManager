import UIKit

final class LoginPresenter:ViewToPresenterLoginProtocol {
    var view: PresenterToViewLoginProtocol?
    var router: PresenterToRouterLoginProtocol?
    var interactor: PresenterToInteractorLoginProtocol?
    
    func touchLoginButton(navigationController: UINavigationController?) {
        
    }
    
    func touchRegisterButton(navigationController: UINavigationController?) {
        router?.openRegisterView(navigationController: navigationController)
    }
    
}




extension LoginPresenter:InteractorToPresenterLoginProtocol {
    
}
