

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b11)
(on b4 b2)
(ontable b5)
(on b6 b5)
(on b7 b10)
(on b8 b9)
(on b9 b7)
(on b10 b6)
(on b11 b1)
(clear b3)
(clear b4)
(clear b8)
)
(:goal
(and
(on b2 b5)
(on b3 b8)
(on b5 b3)
(on b6 b1)
(on b7 b11)
(on b9 b7)
(on b10 b4))
)
)


