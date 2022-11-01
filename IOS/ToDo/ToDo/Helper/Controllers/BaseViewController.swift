import UIKit

class BaseViewController:UIViewController {
    
    override func viewDidLoad() {
        self.addViews()
        self.layoutViews()
        self.configure()
    }
}


@objc extension BaseViewController {
    func addViews() {}
    func layoutViews() {}
    func configure() {}
}
