

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b5)
(on b3 b10)
(on-table b4)
(on-table b5)
(on-table b6)
(on b7 b6)
(on b8 b11)
(on b9 b2)
(on-table b10)
(on b11 b1)
(clear b4)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b8)
(on b3 b2)
(on b4 b6)
(on b5 b9)
(on b7 b5)
(on b9 b3)
(on b10 b11)
(on b11 b4))
)
)


