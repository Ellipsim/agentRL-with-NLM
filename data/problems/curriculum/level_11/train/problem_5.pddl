

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b2)
(on b4 b6)
(on b5 b9)
(on-table b6)
(on-table b7)
(on b8 b7)
(on-table b9)
(on-table b10)
(on b11 b4)
(on b12 b10)
(clear b1)
(clear b3)
(clear b5)
(clear b8)
(clear b11)
(clear b12)
)
(:goal
(and
(on b1 b10)
(on b2 b11)
(on b3 b7)
(on b4 b2)
(on b5 b3)
(on b8 b9)
(on b11 b1))
)
)


