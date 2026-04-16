(set-logic ALL)
; Constraint ID: 75465dc3771b5396
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60091)) (False)
(assert (not (= x 60091)))

; Query: ((== x 60092)) (False)
(assert (not (not (= x 60092))))

(check-sat)
(get-model)
