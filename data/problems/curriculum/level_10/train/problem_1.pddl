

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b9)
(on-table b3)
(on-table b4)
(on-table b5)
(on b6 b11)
(on-table b7)
(on b8 b10)
(on b9 b4)
(on b10 b7)
(on b11 b2)
(clear b1)
(clear b3)
(clear b5)
(clear b8)
)
(:goal
(and
(on b1 b8)
(on b2 b9)
(on b3 b2)
(on b5 b1)
(on b6 b11)
(on b7 b4)
(on b8 b10)
(on b9 b5))
)
)


