

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b1)
(on-table b3)
(on b4 b5)
(on b5 b2)
(on b6 b12)
(on-table b7)
(on b8 b11)
(on b9 b7)
(on b10 b6)
(on b11 b13)
(on-table b12)
(on b13 b10)
(clear b3)
(clear b4)
(clear b9)
)
(:goal
(and
(on b2 b8)
(on b3 b2)
(on b4 b12)
(on b5 b7)
(on b7 b13)
(on b8 b5)
(on b10 b11)
(on b12 b6)
(on b13 b9))
)
)


