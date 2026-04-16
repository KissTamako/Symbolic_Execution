(set-logic ALL)
; Constraint ID: f1082a002dc13e14
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60367)) (False)
(assert (not (= x 60367)))

; Query: ((== x 60368)) (False)
(assert (not (not (= x 60368))))

(check-sat)
(get-model)
