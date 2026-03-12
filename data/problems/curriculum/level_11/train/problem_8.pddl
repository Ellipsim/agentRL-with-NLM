

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b9)
(on b3 b4)
(on b4 b1)
(on-table b5)
(on-table b6)
(on b7 b3)
(on b8 b13)
(on b9 b8)
(on b10 b2)
(on-table b11)
(on b12 b6)
(on b13 b5)
(clear b7)
(clear b10)
(clear b12)
)
(:goal
(and
(on b2 b7)
(on b3 b2)
(on b4 b8)
(on b5 b3)
(on b6 b13)
(on b8 b11)
(on b10 b4)
(on b12 b10)
(on b13 b9))
)
)


