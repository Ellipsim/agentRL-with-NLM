

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b2)
(on b4 b8)
(on b5 b3)
(ontable b6)
(on b7 b6)
(ontable b8)
(on b9 b11)
(on b10 b4)
(on b11 b7)
(clear b1)
(clear b5)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b3 b5)
(on b4 b1)
(on b5 b4)
(on b6 b8)
(on b7 b11)
(on b10 b3)
(on b11 b6))
)
)


