(set-logic ALL)
; Constraint ID: ce350a2892b78d5b
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60679)) (False)
(assert (not (= x 60679)))

; Query: ((== x 60680)) (False)
(assert (not (not (= x 60680))))

(check-sat)
(get-model)
