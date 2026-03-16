

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b7)
(ontable b4)
(on b5 b4)
(ontable b6)
(on b7 b8)
(ontable b8)
(on b9 b6)
(on b10 b11)
(on b11 b5)
(clear b1)
(clear b3)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b7)
(on b2 b11)
(on b4 b9)
(on b5 b3)
(on b6 b10)
(on b7 b5)
(on b8 b2)
(on b9 b6)
(on b11 b1))
)
)


