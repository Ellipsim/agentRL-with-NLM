

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b11)
(on b4 b10)
(ontable b5)
(on b6 b2)
(on b7 b8)
(on b8 b3)
(on b9 b4)
(on b10 b1)
(ontable b11)
(clear b5)
(clear b6)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b7)
(on b2 b1)
(on b4 b5)
(on b5 b10)
(on b7 b8)
(on b8 b4)
(on b9 b6)
(on b11 b2))
)
)


