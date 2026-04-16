(set-logic ALL)
; Constraint ID: 00b545430dc819e0
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59632)) (False)
(assert (not (= x 59632)))

; Query: ((== x 59633)) (False)
(assert (not (not (= x 59633))))

(check-sat)
(get-model)
