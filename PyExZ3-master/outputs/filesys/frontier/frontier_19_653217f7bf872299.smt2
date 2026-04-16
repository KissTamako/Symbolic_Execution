(set-logic ALL)
; Constraint ID: 653217f7bf872299
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60013)) (False)
(assert (not (= x 60013)))

; Query: ((== x 60014)) (False)
(assert (not (not (= x 60014))))

(check-sat)
(get-model)
