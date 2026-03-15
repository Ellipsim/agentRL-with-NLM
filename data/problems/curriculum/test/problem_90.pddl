

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b1)
(on b3 b10)
(on b4 b11)
(on-table b5)
(on b6 b2)
(on b7 b12)
(on b8 b6)
(on b9 b8)
(on-table b10)
(on-table b11)
(on b12 b4)
(clear b3)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b12)
(on b2 b8)
(on b3 b2)
(on b5 b11)
(on b6 b10)
(on b7 b3)
(on b9 b5)
(on b11 b1)
(on b12 b4))
)
)


