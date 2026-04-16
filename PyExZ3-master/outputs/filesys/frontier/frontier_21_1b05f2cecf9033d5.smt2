(set-logic ALL)
; Frontier Constraint ID: 1b05f2cecf9033d5
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 517)) (False)
(assert (not (= x 517)))

; Query: ((== x 518)) (False)
(assert (not (not (= x 518))))

(check-sat)
(get-model)
