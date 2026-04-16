(set-logic ALL)
; Frontier Constraint ID: c3b7217c4ae781c1
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1189)) (False)
(assert (not (= x 1189)))

; Query: ((== x 1190)) (False)
(assert (not (not (= x 1190))))

(check-sat)
(get-model)
