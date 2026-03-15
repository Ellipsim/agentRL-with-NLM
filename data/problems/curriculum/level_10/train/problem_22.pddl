

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b10)
(on b2 b1)
(on-table b3)
(on b4 b12)
(on b5 b2)
(on-table b6)
(on b7 b5)
(on b8 b4)
(on b9 b7)
(on b10 b11)
(on b11 b6)
(on-table b12)
(clear b3)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b12)
(on b2 b4)
(on b3 b8)
(on b4 b7)
(on b5 b6)
(on b6 b2)
(on b9 b5)
(on b11 b1)
(on b12 b10))
)
)


