(set-logic ALL)
; Constraint ID: 162673741bcfaab4
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60214)) (False)
(assert (not (= x 60214)))

; Query: ((== x 60215)) (False)
(assert (not (not (= x 60215))))

(check-sat)
(get-model)
